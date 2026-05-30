"""
make_sample.py — Genera una MUESTRA SINTÉTICA de indicadores de seguridad por
región y semestre, con la misma estructura que tendría un consolidado de INEI /
OBNASEC. Permite ejecutar el proyecto sin conexión y producir el tablero.

Los datos NO son reales. Calibrados en rangos plausibles para demostración.
"""
import numpy as np
import pandas as pd

import config


def _semestres(inicio="2018-S1", fin="2025-S2"):
    a0, s0 = int(inicio[:4]), int(inicio[-1])
    a1, s1 = int(fin[:4]), int(fin[-1])
    out = []
    a, s = a0, s0
    while (a, s) <= (a1, s1):
        out.append(f"{a}-S{s}")
        s = 1 if s == 2 else 2
        if s == 1:
            a += 1
    return out


def generar_muestra(semilla=7):
    rng = np.random.default_rng(semilla)
    periodos = _semestres(config.PERIODO_INICIO, "2025-S2")
    regiones = list(config.REGIONES.keys())

    # Nivel base de victimización por región (algunas estructuralmente más altas).
    base_vict = {r: rng.uniform(16, 32) for r in regiones}
    # Lima, Callao, Arequipa, La Libertad tienden a ser más altas.
    for r in ["Lima", "Callao", "Arequipa", "La Libertad", "Junín", "Cusco"]:
        base_vict[r] = rng.uniform(26, 34)

    filas = []
    for i, periodo in enumerate(periodos):
        tendencia = 1 + 0.004 * i  # leve alza temporal
        for r in regiones:
            vict = np.clip(base_vict[r] * tendencia * rng.normal(1, 0.05), 8, 45)
            homi = np.clip((vict / 6) * rng.normal(1, 0.15), 1, 15)
            perc = np.clip(vict * rng.uniform(2.4, 2.9), 40, 95)
            pobl = int(rng.uniform(0.2, 10) * 1_000_000)
            denun = int(vict / 100 * pobl * rng.uniform(0.05, 0.12))
            filas.append({
                "region": r,
                "periodo": periodo,
                "tasa_victimizacion": round(float(vict), 1),
                "tasa_homicidios": round(float(homi), 1),
                "percepcion_inseguridad": round(float(perc), 1),
                "denuncias": denun,
                "poblacion": pobl,
            })
    df = pd.DataFrame(filas)
    df["fuente"] = "MUESTRA SINTÉTICA (no es dato real)"
    return df


if __name__ == "__main__":
    df = generar_muestra()
    df.to_csv(config.RUTA_MUESTRA, index=False)
    print(f"Muestra sintética: {config.RUTA_MUESTRA} "
          f"({len(df)} filas, {df['region'].nunique()} regiones, "
          f"{df['periodo'].nunique()} periodos)")
