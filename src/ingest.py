"""
ingest.py — Obtiene el consolidado de indicadores de seguridad por región.

Estrategia de automatización:
  - Si config.FUENTE_URL apunta a un CSV publicado (INEI / datos abiertos),
    lo descarga y normaliza columnas.
  - Si no hay URL o falla la descarga, usa la muestra sintética.
  - Pensado para correr de forma programada (GitHub Actions / cron) y refrescar
    el dato cada vez que INEI/OBNASEC publican un nuevo periodo.

Uso:
    python -m src.ingest --refresh    # intenta descargar de la fuente real
    python -m src.ingest              # modo muestra (offline)
"""
import argparse
import sys

import pandas as pd
import requests

import config

# Mapeo flexible: nombres de columna esperados <- posibles variantes de la fuente.
COLUMNAS_ESPERADAS = ["region", "periodo", "tasa_victimizacion",
                      "tasa_homicidios", "percepcion_inseguridad",
                      "denuncias", "poblacion"]


def _normalizar(df):
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    faltantes = [c for c in COLUMNAS_ESPERADAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"La fuente no trae las columnas esperadas: {faltantes}. "
                         f"Ajusta el mapeo en ingest._normalizar().")
    return df[COLUMNAS_ESPERADAS]


def descargar_en_vivo():
    if not config.FUENTE_URL:
        raise RuntimeError("config.FUENTE_URL está vacío.")
    resp = requests.get(config.FUENTE_URL, timeout=60)
    resp.raise_for_status()
    from io import StringIO
    df = pd.read_csv(StringIO(resp.text))
    df = _normalizar(df)
    df["fuente"] = config.FUENTE_NOMBRE
    return df


def cargar_muestra():
    import os
    if not os.path.exists(config.RUTA_MUESTRA):
        from src.make_sample import generar_muestra
        generar_muestra().to_csv(config.RUTA_MUESTRA, index=False)
    return pd.read_csv(config.RUTA_MUESTRA)


def ingestar(refresh=False):
    if refresh:
        try:
            df = descargar_en_vivo()
            print(f"[ingest] Descarga en vivo OK: {len(df)} filas.")
        except Exception as e:  # noqa: BLE001
            print(f"[ingest] Sin fuente en vivo ({e}). Uso la muestra sintética.",
                  file=sys.stderr)
            df = cargar_muestra()
    else:
        df = cargar_muestra()
        print(f"[ingest] Modo offline: {len(df)} filas (muestra sintética).")

    df.to_csv(config.RUTA_CRUDO, index=False)
    print(f"[ingest] Guardado en {config.RUTA_CRUDO}")
    return df


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ingestar(refresh=ap.parse_args().refresh)
