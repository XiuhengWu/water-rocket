"""
Parameterstudie Startdruck:
Dieses Skript untersucht den Einfluss des Startdrucks auf die maximale Flughöhe der Wasserrakete
bei konstantem Wasservolumen. Für verschiedene Startdrücke werden Simulationen durchgeführt und die Ergebnisse grafisch dargestellt.
"""

import numpy as np
import matplotlib.pyplot as plt
import rocket_sim

# ---------------------------
# Parameterbereich
# ---------------------------
drucke = np.arange(0, 20, 0.1)  # Druck von 1 bis 20 bar
max_hoehen = np.zeros(len(drucke))

# ---------------------------
# Simulationen durchführen
# ---------------------------

print("Starte Simulationen...")
for i, druck in enumerate(drucke):
    rocket_sim.druck_initial = druck * 100000
    rocket_sim.initial_luft_volumen = rocket_sim.total_volumen - rocket_sim.wasservolumen_initial

    _, höhen, _, _, _, _, _, _, _, _, _ = rocket_sim.run_simulation(None)
    max_hoehen[i] = np.max(höhen) if höhen else 0

    # Fortschrittsanzeige bei 10% Schritten
    if i % (len(drucke)//10) == 0:
        print(f"Fortschritt: {i/len(drucke)*100:.0f}%")

# ---------------------------
# Diagrammerstellung
# ---------------------------
plt.figure(figsize=(11, 6))

plt.plot(drucke, max_hoehen, '-', color='#1f77b4', linewidth=1.5, alpha=0.9,
         label='Maximale Flughöhe')

plt.axvline(x=8, color='red', linestyle='--', linewidth=2)
plt.text(8 + 0.1, plt.ylim()[1]*0.95, 'Maximaler Sicherheitsdruck\n(8 bar)', color='red', va='top', fontsize=11)

plt.xlabel('Startdruck [bar]', fontsize=12, labelpad=10)
plt.ylabel('Maximale Höhe [m]', fontsize=12, labelpad=10)
plt.title(f'Maximale Flughöhe in Abhängigkeit vom Startdruck',
          fontsize=14, pad=15)

plt.xticks(np.arange(drucke[0], drucke[-1] + 0.1, 1))
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(0.2))
plt.yticks(np.arange(0, max(max_hoehen)*1.1, 5))

plt.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.5)
plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.3)
plt.gca().set_axisbelow(True)

plt.legend(loc='upper right', fontsize=11)
plt.xlim(drucke[0], drucke[-1])
plt.ylim(0, max(max_hoehen)*1.1)
plt.tight_layout()
plt.show()