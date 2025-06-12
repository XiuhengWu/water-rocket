import pandas as pd
import matplotlib.pyplot as plt
import rocket_sim

# 1. HTML‑Tabelle einlesen
with open("flugdaten.md", "r", encoding="utf-8") as f:
    html_content = f.read()
df = pd.read_html(html_content)[0]

# 2. Prozentuale Umrechnung
df["Masse_pct"] = df["Masse [kg]"] / df["Masse [kg]"].iloc[0] * 100
df["Druck_pct"] = (df["Druck [Pa]"]-rocket_sim.atmosphärendruck) / (rocket_sim.druck_initial-rocket_sim.atmosphärendruck) * 100
df["Beschleunigung_pct"] = df["Beschleunigung [m/s²]"] / df["Beschleunigung [m/s²]"].iloc[0] * 100
df["Schubkraft_pct"] = df["Schubkraft [N]"] / df["Schubkraft [N]"].iloc[0] * 100

# 3. Diagramm zeichnen
plt.figure()

# Farbbereiche markieren
plt.axvspan(df["Zeit [s]"].min(), 0.074, color="#b3e0ff", alpha=0.4)  # hellblau
plt.axvspan(0.074, 0.153, color="#ffb3b3", alpha=0.4)      # hellrot
plt.axvspan(0.153, df["Zeit [s]"].max(), color="#e0b3ff", alpha=0.4) # hellviolett

plt.plot(df["Zeit [s]"], df["Masse_pct"], label="Masse")
plt.plot(df["Zeit [s]"], df["Druck_pct"], label="Druckunterschied (relativ zu Atm.)")
plt.plot(df["Zeit [s]"], df["Beschleunigung_pct"], label="Beschleunigung")
plt.plot(df["Zeit [s]"], df["Schubkraft_pct"], label="Schubkraft")

# # Ableitungen berechnen
# druck_diff = df["Druck_pct"].diff() / df["Zeit [s]"].diff()
# masse_diff = df["Masse_pct"].diff() / df["Zeit [s]"].diff()
# for val in df["Masse_pct"][:100]:
#     print(val)
# for val in masse_diff[:100]:
#     print(val)

# # Ableitungen plotten
# plt.plot(df["Zeit [s]"], druck_diff / 100, label="d(Druck_pct-Atm)/dt", linestyle="--", color="orange")
# plt.plot(df["Zeit [s]"], masse_diff / 100, label="dMasse_pct/dt", linestyle="--", color="purple")

plt.xlabel("Zeit [s]")
plt.ylabel("Prozent")
plt.title("Prozentuale Entwicklung der Messgrößen über der Zeit")
plt.legend()
plt.grid(True)
plt.show()