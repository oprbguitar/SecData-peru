"""
build_web.py — Empaqueta los resultados en docs/data.json, el único insumo que
consume el tablero estático (docs/index.html). Así el dashboard funciona en
GitHub Pages o abierto localmente, sin servidor.
"""
import json

import pandas as pd

import config


def construir():
    df = pd.read_csv(config.RUTA_PROCESADO)
    snap = pd.read_csv(config.RUTA_SNAPSHOT)

    ultimo = sorted(df["periodo"].unique(), key=lambda p: (int(p[:4]), int(p[-1])))[-1]
    periodos = sorted(df["periodo"].unique(), key=lambda p: (int(p[:4]), int(p[-1])))

    # Hotspots (último periodo) para el mapa de puntos.
    hotspots = [{
        "region": r.region,
        "lat": r.lat, "lon": r.lon,
        "victimizacion": r.tasa_victimizacion,
        "homicidios": r.tasa_homicidios,
        "percepcion": r.percepcion_inseguridad,
        "riesgo": r.indice_riesgo,
        "semaforo": r.semaforo,
        "var_pp": (None if pd.isna(r.var_vict_pp) else r.var_vict_pp),
    } for r in snap.itertuples()]

    # Series temporales por región (para el gráfico de tendencia).
    series = {}
    for region, g in df.sort_values("periodo").groupby("region"):
        series[region] = {
            "periodos": list(g["periodo"]),
            "victimizacion": list(g["tasa_victimizacion"]),
            "homicidios": list(g["tasa_homicidios"]),
        }

    # Tendencia nacional (promedio simple por periodo).
    nacional = (df.groupby("periodo")["tasa_victimizacion"].mean()
                .reindex(periodos).round(1))

    # Ranking del último periodo.
    ranking = [{"region": r.region, "riesgo": r.indice_riesgo,
                "semaforo": r.semaforo} for r in snap.itertuples()]

    # Frames por periodo (para animar el mapa a lo largo del tiempo).
    coords = config.REGIONES
    por_periodo = {}
    for periodo, g in df.groupby("periodo"):
        por_periodo[periodo] = [{
            "region": row.region,
            "lat": coords[row.region][0], "lon": coords[row.region][1],
            "victimizacion": row.tasa_victimizacion,
            "homicidios": row.tasa_homicidios,
            "riesgo": row.indice_riesgo,
            "semaforo": row.semaforo,
        } for row in g.itertuples()]

    salida = {
        "meta": {
            "ultimo_periodo": ultimo,
            "fuente": config.FUENTE_NOMBRE,
            "indicador_principal": "Tasa de victimización (%)",
            "semaforo_umbrales": config.SEMAFORO,
        },
        "hotspots": hotspots,
        "ranking": ranking,
        "nacional": {"periodos": periodos, "victimizacion": list(nacional.values)},
        "series": series,
        "por_periodo": por_periodo,
    }
    with open(config.RUTA_WEB_JSON, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=2)
    print(f"[build_web] Tablero alimentado: {config.RUTA_WEB_JSON} "
          f"({len(hotspots)} regiones, último periodo {ultimo})")


if __name__ == "__main__":
    construir()
