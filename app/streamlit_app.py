"""
streamlit_app.py — Tablero interactivo local de SeguridadData Perú.

Ejecutar:
    streamlit run app/streamlit_app.py

Mapa de hotspots, filtro por semáforo, ranking y tendencia por región.
"""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parents[1]))
import config  # noqa: E402

st.set_page_config(page_title="SeguridadData Perú", layout="wide")
st.title("🛡️ SeguridadData Perú")
st.caption("Hotspots de inseguridad por región · tablero para toma de decisiones. "
           "Fuente: INEI / OBNASEC (demo con muestra sintética).")

COL = {"Alto": "#e4572e", "Medio": "#f2a900", "Bajo": "#3fb27f"}


@st.cache_data
def cargar():
    df = pd.read_csv(config.RUTA_PROCESADO)
    snap = pd.read_csv(config.RUTA_SNAPSHOT)
    return df, snap


try:
    df, snap = cargar()
except FileNotFoundError:
    st.warning("Ejecuta primero: `python -m src.run_pipeline`")
    st.stop()

ultimo = snap["periodo"].iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric("Victimización promedio nacional", f"{snap['tasa_victimizacion'].mean():.1f} %")
c2.metric("Mayor riesgo", f"{snap.iloc[0]['region']}", f"índice {snap.iloc[0]['indice_riesgo']:.0f}")
c3.metric("Regiones en nivel Alto", int((snap["semaforo"] == "Alto").sum()))

niveles = st.multiselect("Filtrar por semáforo", ["Alto", "Medio", "Bajo"],
                         default=["Alto", "Medio", "Bajo"])
snap_f = snap[snap["semaforo"].isin(niveles)]

izq, der = st.columns([1.4, 1])
with izq:
    st.subheader(f"Mapa de hotspots · {ultimo}")
    mapa = snap_f.rename(columns={"lat": "latitude", "lon": "longitude"}).copy()
    mapa["color"] = mapa["semaforo"].map(COL)
    st.map(mapa, latitude="latitude", longitude="longitude", size="indice_riesgo", color="color")
with der:
    st.subheader("Ranking de riesgo")
    st.dataframe(
        snap_f[["region", "indice_riesgo", "tasa_victimizacion", "semaforo"]]
        .reset_index(drop=True),
        use_container_width=True, hide_index=True,
    )

st.subheader("Tendencia de victimización")
region = st.selectbox("Región", ["Nacional"] + sorted(df["region"].unique()))
if region == "Nacional":
    serie = df.groupby("periodo")["tasa_victimizacion"].mean()
else:
    serie = df[df["region"] == region].set_index("periodo")["tasa_victimizacion"]
st.line_chart(serie)

st.info("Lectura para decisión: el índice de riesgo combina victimización, "
        "homicidios y percepción de inseguridad (pesos configurables). El semáforo "
        "permite priorizar dónde concentrar patrullaje, presupuesto o intervención.")
