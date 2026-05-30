"""
SeguridadData Perú — Configuración central
------------------------------------------
Fuentes públicas de criminalidad y victimización:

  - INEI Data-Crim  : Sistema Integrado de Estadísticas de la Criminalidad y
                      Seguridad Ciudadana (victimización, denuncias, procesos).
                      https://www.gob.pe/inei  (Data-Crim)
  - INEI SIRTOD     : Sistema de Información Regional para la Toma de Decisiones
                      (indicadores regional/provincial/distrital).
  - INEI ENAPRES    : Encuesta de victimización (microdatos descargables; también
                      publicada en la Plataforma Nacional de Datos Abiertos).
  - OBNASEC (Mininter): Observatorio Nacional de Seguridad Ciudadana
                      https://observatorio.mininter.gob.pe (Indicadores, Mapas, Base de Datos)

Cadencia real de los datos: la victimización (ENAPRES) es SEMESTRAL/anual y los
indicadores del OBNASEC son periódicos. No existe un feed "en vivo" minuto a
minuto; la automatización consiste en refrescar el último dataset publicado de
forma programada (ver .github/workflows/refresh.yml).
"""

# ---------------------------------------------------------------------------
# 1) Fuente de datos (configurable). Reemplaza por la URL real del CSV/Excel
#    publicado en datos abiertos / INEI cuando lo tengas identificado.
# ---------------------------------------------------------------------------
FUENTE_URL = ""  # p.ej. un CSV de datosabiertos.gob.pe; vacío => modo muestra
FUENTE_NOMBRE = "INEI ENAPRES / OBNASEC (demostración con muestra sintética)"

# ---------------------------------------------------------------------------
# 2) Regiones del Perú con centroides aproximados (lat, lon) para el mapa de
#    puntos (hotspots). 24 departamentos + Provincia Constitucional del Callao.
# ---------------------------------------------------------------------------
REGIONES = {
    "Amazonas":        (-5.20, -78.00),
    "Áncash":          (-9.50, -77.50),
    "Apurímac":        (-14.00, -72.90),
    "Arequipa":        (-16.40, -72.30),
    "Ayacucho":        (-13.90, -74.00),
    "Cajamarca":       (-6.50, -78.50),
    "Callao":          (-12.05, -77.12),
    "Cusco":           (-13.50, -71.90),
    "Huancavelica":    (-12.90, -74.90),
    "Huánuco":         (-9.50, -76.00),
    "Ica":             (-14.20, -75.70),
    "Junín":           (-11.50, -75.00),
    "La Libertad":     (-8.00, -78.50),
    "Lambayeque":      (-6.40, -79.80),
    "Lima":            (-11.80, -76.80),
    "Loreto":          (-4.00, -74.50),
    "Madre de Dios":   (-12.00, -70.50),
    "Moquegua":        (-16.80, -70.90),
    "Pasco":           (-10.50, -75.50),
    "Piura":           (-5.20, -80.00),
    "Puno":            (-15.00, -70.00),
    "San Martín":      (-7.00, -76.70),
    "Tacna":           (-17.80, -70.30),
    "Tumbes":          (-3.80, -80.40),
    "Ucayali":         (-9.50, -73.50),
}

# ---------------------------------------------------------------------------
# 3) Indicadores que maneja el tablero
# ---------------------------------------------------------------------------
INDICADORES = {
    "tasa_victimizacion": "Tasa de victimización (% de personas 15+ víctimas en 12 meses)",
    "tasa_homicidios": "Tasa de homicidios (por 100 mil hab.)",
    "denuncias": "Denuncias registradas (conteo)",
    "percepcion_inseguridad": "Percepción de inseguridad (%)",
}

# Umbrales de semáforo para el indicador principal (victimización %).
# Ajustables según la lectura de política que se quiera dar.
SEMAFORO = {
    "alto": 28.0,    # >= 28 %  -> rojo
    "medio": 22.0,   # 22–28 %  -> ámbar  ; < 22 % -> verde
}

# Pesos del índice compuesto de riesgo (hotspot score 0–100).
PESOS_RIESGO = {
    "tasa_victimizacion": 0.45,
    "tasa_homicidios": 0.35,
    "percepcion_inseguridad": 0.20,
}

PERIODO_INICIO = "2018-S1"
HORIZONTE_PROYECCION = 1  # próximo semestre

# ---------------------------------------------------------------------------
# 4) Rutas de salida
# ---------------------------------------------------------------------------
RUTA_MUESTRA = "data_open/_muestra_sintetica.csv"
RUTA_CRUDO = "data_open/seguridad_regional.csv"
RUTA_PROCESADO = "data_processed/indicadores_regionales.csv"
RUTA_SNAPSHOT = "data_processed/snapshot_ultimo_periodo.csv"
RUTA_WEB_JSON = "docs/data.json"
