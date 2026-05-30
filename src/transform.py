"""
transform.py — Construye la capa de decisión:
  - variación vs. periodo anterior (puntos porcentuales)
  - índice compuesto de riesgo (0–100) por región
  - clasificación semáforo (Alto / Medio / Bajo) para lectura inmediata
  - snapshot del último periodo (insumo del mapa de hotspots)
"""
import numpy as np
import pandas as pd

import config


def _orden_periodo(p):
    a, s = p.split("-S")
    return int(a) * 10 + int(s)




def transformar(df):
    df = df.copy()
    df["orden"] = df["periodo"].map(_orden_periodo)
    df = df.sort_values(["region", "orden"])

    # Variación de la victimización vs. periodo anterior (puntos porcentuales).
    df["var_vict_pp"] = df.groupby("region")["tasa_victimizacion"].diff().round(1)

    # Índice compuesto de riesgo dentro de CADA periodo (comparabilidad regional).
    # Normalización min-max por periodo con groupby.transform (robusto entre versiones).
    def norm_por_periodo(col):
        gmin = df.groupby("periodo")[col].transform("min")
        gmax = df.groupby("periodo")[col].transform("max")
        rng = (gmax - gmin).replace(0, np.nan)
        return ((df[col] - gmin) / rng * 100).fillna(0)

    df["indice_riesgo"] = (
        config.PESOS_RIESGO["tasa_victimizacion"] * norm_por_periodo("tasa_victimizacion")
        + config.PESOS_RIESGO["tasa_homicidios"] * norm_por_periodo("tasa_homicidios")
        + config.PESOS_RIESGO["percepcion_inseguridad"] * norm_por_periodo("percepcion_inseguridad")
    ).round(1)

    # Semáforo según umbrales sobre la victimización.
    def clasificar(v):
        if v >= config.SEMAFORO["alto"]:
            return "Alto"
        if v >= config.SEMAFORO["medio"]:
            return "Medio"
        return "Bajo"

    df["semaforo"] = df["tasa_victimizacion"].map(clasificar)
    df = df.drop(columns=["orden"])
    df.to_csv(config.RUTA_PROCESADO, index=False)
    print(f"[transform] Indicadores guardados en {config.RUTA_PROCESADO} ({len(df)} filas)")

    # Snapshot del último periodo (para el mapa).
    ultimo = df.sort_values("periodo")["periodo"].iloc[-1]
    snap = df[df["periodo"] == ultimo].copy()
    snap["lat"] = snap["region"].map(lambda r: config.REGIONES[r][0])
    snap["lon"] = snap["region"].map(lambda r: config.REGIONES[r][1])
    snap = snap.sort_values("indice_riesgo", ascending=False)
    snap.to_csv(config.RUTA_SNAPSHOT, index=False)
    print(f"[transform] Snapshot ({ultimo}) guardado en {config.RUTA_SNAPSHOT}")
    return df, snap


if __name__ == "__main__":
    crudo = pd.read_csv(config.RUTA_CRUDO)
    transformar(crudo)
