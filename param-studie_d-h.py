"""
Parameterstudie Düsendurchmesser:
Dieses Skript untersucht den Einfluss des Düsendurchmessers auf die maximale Flughöhe der Wasserrakete.
Für verschiedene Düsendurchmesser werden Simulationen durchgeführt und die Ergebnisse grafisch dargestellt.
"""

import numpy as np
import matplotlib.pyplot as plt
import rocket_sim

# ---------------------------
# Parameterbereich
# ---------------------------
duesen = np.arange(10, 80, 0.5)  # Düsendurchmesser von 10 mm bis 80 mm
max_hoehen = np.zeros(len(duesen))

# ---------------------------
# Simulationen durchführen
# ---------------------------

print("Starte Simulationen...")
for i, d in enumerate(duesen):
    rocket_sim.initial_luft_volumen = rocket_sim.total_volumen - rocket_sim.wasservolumen_initial
    rocket_sim.düsendurchmesser = d / 1000  # Umrechnung mm -> m
    rocket_sim.düsenfläche = np.pi * (rocket_sim.düsendurchmesser/2)**2

    _, höhen, _, _, _, _, _, _, _, _, _ = rocket_sim.run_simulation(None)
    max_hoehen[i] = np.max(höhen) if höhen else 0

    if i % (len(duesen)//10) == 0:
        print(f"Fortschritt: {i/len(duesen)*100:.0f}%")

# ---------------------------
# Diagrammerstellung
# ---------------------------
plt.figure(figsize=(11, 6))

plt.plot(duesen, max_hoehen, '-', color='#1f77b4', linewidth=1.5, alpha=0.9,
         label='Maximale Flughöhe')


plt.xlabel('Düsendurchmesser [mm]', fontsize=12, labelpad=10)
plt.ylabel('Maximale Höhe [m]', fontsize=12, labelpad=10)
plt.title(f'Maximale Flughöhe in Abhängigkeit vom Düsendurchmesser',
          fontsize=14, pad=15)

plt.xticks(np.arange(duesen[0], duesen[-1] + 0.1, 5))  # Schrittweite auf 5 mm erhöht
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))  # Minor-Ticks auf 1 mm gesetzt
plt.yticks(np.arange(0, max(max_hoehen)*1.1, 5))

plt.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.5)
plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.3)
plt.gca().set_axisbelow(True)

plt.legend(loc='upper right', fontsize=11)
plt.xlim(duesen[0], duesen[-1])
plt.ylim(0, max(max_hoehen)*1.1)
plt.tight_layout()
plt.show()