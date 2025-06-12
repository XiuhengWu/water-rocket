"""
Parameterstudie Wasserrakete:
Dieses Skript untersucht den Einfluss des anfänglichen Wasservolumens auf die maximale Flughöhe der Rakete
bei konstantem Druck. Es führt für verschiedene Wasservolumina Simulationen durch und visualisiert das Ergebnis.
"""

import numpy as np
import matplotlib.pyplot as plt
import rocket_sim

# ---------------------------
# Parameterbereich
# ---------------------------
wasser_vols = np.arange(0.0, 1.5, 0.01)
max_hoehen = np.zeros(len(wasser_vols))

# ---------------------------
# Simulationen durchführen
# ---------------------------

print("Starte Simulationen...")
for i, wasser_vol in enumerate(wasser_vols):
    rocket_sim.wasservolumen_initial = wasser_vol / 1000
    rocket_sim.initial_luft_volumen = rocket_sim.total_volumen - rocket_sim.wasservolumen_initial
    
    _, höhen, _, _, _, _, _, _, _, _, _ = rocket_sim.run_simulation(None)
    max_hoehen[i] = max(höhen) if höhen else 0
    
    # Fortschrittsanzeige bei 10% Schritten
    if i % (len(wasser_vols)//10) == 0:
        print(f"Fortschritt: {i/len(wasser_vols)*100:.0f}%")


# ---------------------------
# Diagrammerstellung
# ---------------------------
plt.figure(figsize=(11, 6))

# Hauptdiagramm mit optimierter Darstellung
plt.plot(wasser_vols, max_hoehen, 
         '-', color='#1f77b4', linewidth=1.5, alpha=0.9,
         label='Maximale Flughöhe')

# Optimum markieren mit Annotation
opt_index = np.argmax(max_hoehen)
plt.plot(wasser_vols[opt_index], max_hoehen[opt_index], 
         'ro', markersize=10, label=f'Optimum ({max_hoehen[opt_index]:.1f}m)')
plt.annotate(f'Optimum: {wasser_vols[opt_index]:.2f} l \n({wasser_vols[opt_index] / (rocket_sim.total_volumen*1000):.1%} des Gesamtvolumens)',
             xy=(wasser_vols[opt_index], max_hoehen[opt_index]),
             xytext=(wasser_vols[opt_index] + 0.05, max_hoehen[opt_index] - 5),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
             fontsize=11, bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8))

# ---------------------------
# Zusätzliche Analyse
# ---------------------------
# Finde den 95%-Bereich des Maximums
threshold = 0.95 * max(max_hoehen)
optimal_range = wasser_vols[max_hoehen >= threshold]
print(f"\nOptimaler Bereich (≥95% des Maximums):")
print(f"Von {optimal_range[0]:.2f} l bis {optimal_range[-1]:.2f} l")

# Optimalen Bereich als Band einzeichnen
if len(optimal_range) > 0:
    plt.axvspan(optimal_range[0], optimal_range[-1], color='lightgreen', alpha=0.2, 
                label='Optimaler Bereich (≥95%)')

# Automatische Achsenskallierung
plt.xlabel('Anfängliches Wasservolumen [l]', fontsize=12, labelpad=10)
plt.ylabel('Maximale Höhe [m]', fontsize=12, labelpad=10)
plt.title(f'Maximale Flughöhe in Abhängigkeit vom Wasservolumen', 
          fontsize=14, pad=15)

# Intelligente Tick-Kontrolle
plt.xticks(np.arange(wasser_vols[0], wasser_vols[-1] + 0.01, 0.1))  # Hauptticks dynamisch
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(0.02))  # Minorticks alle 0.02 l
plt.yticks(np.arange(0, max(max_hoehen)*1.1, 5))  # Y-Ticks in 5m-Schritten

# Raster und Hintergrund optimieren
plt.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.5)
plt.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.3)
plt.gca().set_axisbelow(True)

# Legende und Layout
plt.legend(loc='upper right', fontsize=11)
plt.xlim(wasser_vols[0], wasser_vols[-1])
plt.ylim(0, max(max_hoehen)*1.1)
plt.tight_layout()

# ---------------------------
# Zusätzliche Analyse
# ---------------------------
# Finde den 95%-Bereich des Maximums
plt.show()
