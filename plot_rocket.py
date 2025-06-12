"""
Visualisierung der Simulation einer Wasserrakete:
Dieses Skript führt die Simulation aus und erstellt verschiedene Diagramme zum Flugverlauf, wie Höhe, Geschwindigkeit,
Beschleunigung, Druck und Masse. Zusätzlich werden wichtige Flugdaten wie Burnout-Zeit, Maximalhöhe und Flugzeit angezeigt.
"""

import matplotlib.pyplot as plt
import numpy as np
from rocket_sim import run_simulation

# Simulation ausführen und Daten erhalten
(
    zeitpunkte,
    höhen,
    geschwindigkeiten,
    beschleunigungen,
    drücke,
    massen,
    schubkräfte,
    _,
    _,
    _,
    _
) = run_simulation(5)

# ---------------------------
# Diagramme
# ---------------------------
fig = plt.figure(figsize=(12, 7))

plt.subplot(3, 2, 1)
plt.plot(zeitpunkte, höhen, color="C0")
plt.title("Flugbahn")
plt.xlabel("Zeit [s]")
plt.ylabel("Höhe [m]")

plt.subplot(3, 2, 2)
plt.plot(zeitpunkte, geschwindigkeiten, color="C0")
plt.title("Geschwindigkeit")
plt.xlabel("Zeit [s]")
plt.ylabel("v [m/s]")

plt.subplot(3, 2, 3)
plt.plot(zeitpunkte, beschleunigungen, color="C0")
plt.title("Beschleunigung")
plt.xlabel("Zeit [s]")
plt.ylabel("a [m/s²]")

plt.subplot(3, 2, 4)
plt.plot(zeitpunkte, drücke, color="C0")
plt.title("Druckverlauf")
plt.xlabel("Zeit [s]")
plt.ylabel("Druck [Pa]")

plt.subplot(3, 2, 5)
plt.plot(zeitpunkte, massen, color="C0")
plt.title("Massenverlauf")
plt.xlabel("Zeit [s]")
plt.ylabel("Masse [kg]")

# Letztes Diagramm (5. Feld)
schubkräfte = np.array(schubkräfte)
burnout_index = np.where(schubkräfte <= 0)[0][0]
burnout_zeit = zeitpunkte[burnout_index]
burnout_geschwindigkeit = geschwindigkeiten[burnout_index]
burnout_höhe = höhen[burnout_index]
burnout_beschleunigung = beschleunigungen[burnout_index]
max_höhe = np.max(höhen)
zeit_max_höhe = zeitpunkte[np.argmax(höhen)]
max_geschwindigkeit = np.max(geschwindigkeiten)
max_beschleunigung = np.max(beschleunigungen)
max_schub = np.max(schubkräfte)
flugzeit = zeitpunkte[-1]

plt.subplot(3, 2, 5)
plt.plot(zeitpunkte, massen)
plt.title("Massenverlauf")
plt.xlabel("Zeit [s]")

# 6. Feld: leeres Subplot für Text
ax_text = plt.subplot(3, 2, 6)
ax_text.axis("off")  # Achsen ausblenden
text = (
    f"Burnout-Zeit: {burnout_zeit:.2f} s\n"
    f"Burnout-Geschwindigkeit: {burnout_geschwindigkeit:.2f} m/s\n"
    f"Burnout-Höhe: {burnout_höhe:.2f} m\n"
    f"Burnout-Beschleunigung: {burnout_beschleunigung:.2f} m/s²\n"
    f"Maximalhöhe: {max_höhe:.2f} m\n"
    f"Zeitpunkt der Maximalhöhe: {zeit_max_höhe:.2f} s\n"
    f"Maximalgeschwindigkeit: {max_geschwindigkeit:.2f} m/s\n"
    f"Maximalbeschleunigung: {max_beschleunigung:.2f} m/s²\n"
    f"Flugzeit: {flugzeit:.2f} s\n"
    f"Maximale Schubkraft: {max_schub:.2f} N\n"
)
ax_text.text(0, 0.5, text, va="center", fontsize=12)

fig.canvas.manager.set_window_title("Raketenflug Simulation")

plt.tight_layout()
plt.show()
