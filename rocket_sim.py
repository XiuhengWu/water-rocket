"""
Simulation einer Wasserrakete:
Dieses Skript simuliert den Flug einer Wasserrakete unter Berücksichtigung von Schubphasen (Wasser- und Luftschub),
Luftwiderstand, Gravitation und weiteren physikalischen Parametern. Die Ergebnisse werden als HTML-Tabelle ausgegeben.
"""

import numpy as np

# ---------------------------
# Physikalische Konstanten
# ---------------------------
g = 9.81                # Erdbeschleunigung [m/s²]
luftdichte = 1.204      # Dichte der Luft [kg/m³]
wasserdichte = 998     # Dichte von Wasser [kg/m³]
atmosphärendruck = 101325 # Atmosphärendruck [Pa]
gamma = 1.4             # Adiabatenindex für Luft
R_spezifisch = 287      # Spezifische Gaskonstante für Luft [J/(kg·K)]
Cd_wasser = 0.97        # Entladungskoeffizient für Wasser
Cd_luft = 0.8           # Entladungskoeffizient für Luft
Cw = 0.5                # Luftwiderstandsbeiwert

# ---------------------------
# Raketenparameter
# ---------------------------
leermasse = 80         # Masse der leeren Rakete [g]
total_volumen = 1.5       # Gesamtvolumen der Rakete [l]
wasservolumen_initial = 0.8  # Anfangsvolumen des Wassers [l]
düsendurchmesser = 22   # Durchmesser der Düse [mm]
druck_initial = 4      # Anfangsdruck in der Rakete [bar]
rocketdurchmesser = 83 # Durchmesser der Rakete [mm]
umgebungstemperatur = 25 # Umgebungstemperatur [C]

# Einheit umwandeln
leermasse = leermasse / 1000                # [g] -> [kg]
total_volumen = total_volumen / 1000        # [l] -> [m³]
wasservolumen_initial = wasservolumen_initial / 1000    # [l] -> [m³]
düsendurchmesser = düsendurchmesser / 1000  # [mm] -> [m]
druck_initial = druck_initial * 100000      # [bar] -> [Pa]
rocketdurchmesser = rocketdurchmesser / 1000    # [mm] -> [m]
umgebungstemperatur = umgebungstemperatur + 273.15  # [C] -> [K]

# Abgeleitete Größen
düsenfläche = np.pi * (düsendurchmesser/2)**2
querschnittsfläche = np.pi * (rocketdurchmesser/2)**2
initial_luft_volumen = total_volumen - wasservolumen_initial

# ---------------------------
# Funktionen für Physik-Berechnungen
# ---------------------------
def Schubkraft(innendruck, düsenfläche, phase):
    """Berechnet die Schubkraft für Wasser oder Luft."""
    delta_p = innendruck - atmosphärendruck
    if delta_p <= 0:
        return 0.0
    
    if phase == "Wasserschubphase":
        return 2 * delta_p * düsenfläche * Cd_wasser   # Schubkraft aus Impulserhaltung
    elif phase == "Luftschubphase":
        return 2 * delta_p * düsenfläche * Cd_luft   # Schubkraft aus Impulserhaltung

def Massenstrom(innendruck, düsenfläche, phase):
    """Berechnet den Massenstrom für Wasser oder Luft."""
    delta_p = innendruck - atmosphärendruck
    if delta_p <= 0:
        return 0.0
    
    if phase == "Wasserschubphase":
        return Cd_wasser * düsenfläche * np.sqrt(2 * wasserdichte * delta_p)   # Massenstrom Formel
    elif phase == "Luftschubphase":
        luftdichte = innendruck / (R_spezifisch * umgebungstemperatur)  # Ideales Gasgesetz
        return Cd_luft * düsenfläche * np.sqrt(2 * luftdichte * delta_p) # Massenstrom Formel
    
def Innendruck(luft_volumen, phase, luft_masse = None, lufttemperatur = None):
    """Berechnet den Druck in der Rakete während der Wasser- und Luftphase."""
    if phase == "Wasserschubphase":
        innendruck = druck_initial * (initial_luft_volumen / luft_volumen)**gamma # Adiabatische Druckabfall
    elif phase == "Luftschubphase":
        if luft_masse <= 0:
            innendruck = atmosphärendruck
        else:
            innendruck = (luft_masse * R_spezifisch * lufttemperatur) / total_volumen   # Ideales Gasgesetz
    return innendruck

def Lufttemperatur(druck, luft_volumen, luftmasse, phase):
    """Berechnet die Temperatur der Luft in der Rakete."""
    lufttemperatur = druck * luft_volumen / (R_spezifisch * luftmasse)  # Ideales Gasgesetz
    return lufttemperatur

def Luftwiderstand(geschwindigkeit, phase):
    """Berechnet den Luftwiderstand."""
    luftwiderstand = -0.5 * luftdichte * Cw * querschnittsfläche * abs(geschwindigkeit) * geschwindigkeit # `abs(geschwindigkeit) * geschwindigkeit`, damit der Widerstand gegen die Bewegungsrichtung wirkt
    return luftwiderstand

def run_simulation(save_every_n_steps=10):
    # ---------------------------
    # Initialisierung
    # ---------------------------
    # Anfangsbedingungen
    wasser_masse = wasservolumen_initial * wasserdichte
    wasser_volumen = wasser_masse / wasserdichte
    luft_masse = (druck_initial * initial_luft_volumen) / (R_spezifisch * umgebungstemperatur)
    lufttemperatur = umgebungstemperatur
    innendruck = druck_initial

    # Simulationsvariablen
    t = 0
    dt = 0.0001 # Zeitschritt [s]
    höhe = 0
    geschwindigkeit = 0
    phase = "Wasserschubphase"

    # Listen für Dateispeicherung
    zeitpunkte = []
    höhen = []
    geschwindigkeiten = []
    beschleunigungen = []
    drücke = []
    massen = []
    schubkräfte = []
    resultierende_kräfte = []
    wasser_volumen_liste = []
    luftwiderstände = []
    gravitationen = []

    # ---------------------------
    # Hauptsimulation
    # ---------------------------
    while True:
        if phase == "Wasserschubphase":
            # Schub und Massenstrom berechnen
            schubkraft = Schubkraft(innendruck, düsenfläche, phase)
            massenstrom = Massenstrom(innendruck, düsenfläche, phase)

            # Masse und Druck aktualisieren
            wasser_masse = max(wasser_masse - massenstrom * dt, 0)
            masse = leermasse + wasser_masse

            # Aktuelles Luftvolumen (während Wasserphase)
            wasser_volumen = wasser_masse / wasserdichte
            luft_volumen = total_volumen - wasser_volumen
            innendruck = Innendruck(luft_volumen, phase)

            # Übergang zur nächste Phase
            if wasser_masse <= 0:
                phase = "Luftschubphase"
                wasser_masse = 0
                wasser_volumen = 0
                masse = leermasse
                lufttemperatur = Lufttemperatur(innendruck, luft_volumen, luft_masse, phase)
                
    
        elif phase == "Luftschubphase":
            # Luftphase: Druck aus idealem Gasgesetz (mit abnehmender Luftmasse)
            innendruck = Innendruck(luft_volumen, phase, luft_masse, lufttemperatur)

            # Schub und Massenstrom berechnen
            schubkraft = Schubkraft(innendruck, düsenfläche, phase)
            massenstrom = Massenstrom(innendruck, düsenfläche, phase)

            # Masse und Druck aktualisieren
            luft_masse = max(luft_masse - massenstrom * dt, 0)

            # Übergang zur nächste Phase
            if innendruck <= atmosphärendruck:
                phase = "Freier Flug"

        elif phase == "Freier Flug":
            schubkraft = 0
            massenstrom = 0
            innendruck = atmosphärendruck
    

        # Kräfte berechnen
        F_gravitation = -masse * g
        F_luftwiderstand = Luftwiderstand(geschwindigkeit, phase)
        F_resultierende = schubkraft + F_gravitation + F_luftwiderstand
        
        # Beschleunigung, Geschwindigkeit und Höhe aktualisieren
        beschleunigung = F_resultierende / masse   #  2. Newtonsche Gesetz
        geschwindigkeit += beschleunigung * dt
        höhe += geschwindigkeit * dt
        
        # Flugdaten speichern
        zeitpunkte.append(t)
        beschleunigungen.append(beschleunigung)
        geschwindigkeiten.append(geschwindigkeit)
        höhen.append(höhe)
        drücke.append(innendruck)
        massen.append(masse)
        schubkräfte.append(schubkraft)
        resultierende_kräfte.append(F_resultierende)
        wasser_volumen_liste.append(wasser_volumen)
        luftwiderstände.append(F_luftwiderstand)
        gravitationen.append(F_gravitation)

        if wasser_volumen == 0:
            pass
        
        # Abbruch bei Landung
        if höhe <= 0:
            break
        
        t += dt

    daten = (zeitpunkte, höhen, geschwindigkeiten, beschleunigungen, drücke, massen, schubkräfte, resultierende_kräfte, wasser_volumen_liste, luftwiderstände, gravitationen)
    if save_every_n_steps:
        write_html_table("flugdaten.md", *daten, save_every_n_steps=save_every_n_steps)
    return daten

def write_html_table(filename, zeitpunkte, höhen, geschwindigkeiten, beschleunigungen, drücke, massen, schubkräfte, resultierende_kräfte, wasser_volumen_liste, luftwiderstände, gravitationen, save_every_n_steps=1):
    """Speichert die Simulationsdaten als HTML-Tabelle mit fixierten Tabellenüberschriften (CSS sticky)."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("""
<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<title>Flugdaten Tabelle</title>
<style>
table {
  border-collapse: collapse;
  width: 100%;
  font-family: Arial, sans-serif;
}
th, td {
  padding: 4px 8px;
  text-align: right;
}
th {
  background: #dbd6c4;
  position: sticky;
  top: 0;
  z-index: 2;
}
th.sep,
td.sep {
  border-left: 1px solid #cfcaba;
  min-width: 2px;
  width: 2px;
  padding: 0;
}
</style>
</head>
<body>
<table>
<thead>
<tr>
  <th>Index</th>
  <th>Zeit [s]</th>
  <th class="sep"></th>
  <th>Höhe [m]</th>
  <th>Geschwindigkeit [m/s]</th>
  <th>Beschleunigung [m/s²]</th>
  <th class="sep"></th>
  <th>Wasservolumen [m³]</th>
  <th>Masse [kg]</th>
  <th>Druck [Pa]</th>
  <th class="sep"></th>
  <th>Schubkraft [N]</th>
  <th>Luftwiderstand [N]</th>
  <th>Gravitation [N]</th>
  <th>Resultierende Kraft [N]</th>
</tr>
</thead>
<tbody>
""")
        for idx, i in enumerate(range(0, len(zeitpunkte), save_every_n_steps)):
            f.write(
                f"<tr>"
                f"<td>{idx}</td>"
                f"<td>{zeitpunkte[i]:.4f}</td>"
                f"<td class='sep'></td>"
                f"<td>{höhen[i]:.5f}</td>"
                f"<td>{geschwindigkeiten[i]:.3f}</td>"
                f"<td>{beschleunigungen[i]:.3f}</td>"
                f"<td class='sep'></td>"
                f"<td>{wasser_volumen_liste[i]:.6f}</td>"
                f"<td>{massen[i]:.3f}</td>"
                f"<td>{drücke[i]:.1f}</td>"
                f"<td class='sep'></td>"
                f"<td>{schubkräfte[i]:.3f}</td>"
                f"<td>{luftwiderstände[i]:.3f}</td>"
                f"<td>{gravitationen[i]:.3f}</td>"
                f"<td>{resultierende_kräfte[i]:.3f}</td>"
                f"</tr>\n"
            )
        f.write("""
</tbody>
</table>
</body>
</html>
""")

if __name__ == "__main__":
    daten = run_simulation(save_every_n_steps=5)
