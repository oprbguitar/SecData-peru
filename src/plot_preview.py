"""
plot_preview.py — Vista previa estática (PNG) del mapa de hotspots y el ranking,
para usar como captura en el README. Replica con matplotlib lo que el tablero
muestra de forma interactiva con Leaflet.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import config

COL = {"Alto": "#e4572e", "Medio": "#f2a900", "Bajo": "#3fb27f"}


def graficar():
    snap = pd.read_csv(config.RUTA_SNAPSHOT)

    fig, (axm, axr) = plt.subplots(1, 2, figsize=(13, 7),
                                   gridspec_kw={"width_ratios": [1.4, 1]})
    fig.patch.set_facecolor("#0e1419")

    # --- Mapa de burbujas ---
    axm.set_facecolor("#161e26")
    for r in snap.itertuples():
        axm.scatter(r.lon, r.lat, s=40 + r.indice_riesgo * 9,
                    c=COL[r.semaforo], alpha=0.65, edgecolors="white", linewidths=0.6)
        if r.indice_riesgo >= 70:
            axm.annotate(r.region, (r.lon, r.lat), color="#e7edf2",
                         fontsize=8, xytext=(4, 4), textcoords="offset points")
    axm.set_title("Hotspots de riesgo por región",
                  color="#e7edf2", fontsize=13, fontweight="bold")
    axm.set_xlabel("Longitud", color="#8aa0b2", fontsize=9)
    axm.set_ylabel("Latitud", color="#8aa0b2", fontsize=9)
    axm.tick_params(colors="#8aa0b2")
    for s in axm.spines.values():
        s.set_color("#2a3744")

    # --- Ranking ---
    axr.set_facecolor("#161e26")
    top = snap.head(12).iloc[::-1]
    axr.barh(top["region"], top["indice_riesgo"],
             color=[COL[s] for s in top["semaforo"]])
    axr.set_title("Top 12 · índice de riesgo (0–100)",
                  color="#e7edf2", fontsize=12, fontweight="bold")
    axr.tick_params(colors="#8aa0b2")
    for s in axr.spines.values():
        s.set_color("#2a3744")

    fig.suptitle(f"SeguridadData Perú — último periodo {snap['periodo'].iloc[0]}",
                 color="#5db0ff", fontsize=15, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig("docs/captura_dashboard.png", dpi=130, facecolor=fig.get_facecolor())
    print("Vista previa guardada en docs/captura_dashboard.png")


if __name__ == "__main__":
    graficar()
