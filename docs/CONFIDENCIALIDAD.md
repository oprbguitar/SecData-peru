# Declaración de confidencialidad y origen de datos

**SeguridadData Perú** es un proyecto **demostrativo de portafolio**.

## Origen de los datos
- **Datos abiertos del Estado peruano**: INEI (Data-Crim, ENAPRES, SIRTOD) y
  Observatorio Nacional de Seguridad Ciudadana (OBNASEC – Mininter). Información
  pública, de libre acceso y reutilización.
- **Datos sintéticos**: la muestra incluida (`data_open/_muestra_sintetica.csv`)
  es generada por software (`src/make_sample.py`). **No corresponde a cifras
  reales**; existe solo para permitir la ejecución offline y las capturas.

## Lo que NO contiene
- No contiene información reservada, confidencial ni de acceso restringido.
- No contiene datos personales de víctimas ni microdatos identificables.
- No reproduce información ni estructuras internas de empleadores actuales o
  anteriores.

## Finalidad
Evidenciar capacidades de analítica institucional, geovisualización para la toma
de decisiones y automatización de datos públicos. Replica **patrones generales**
de análisis de seguridad ciudadana aplicables a cualquier entidad.

## Buenas prácticas aplicadas
- Trabajo con datos **agregados por región**, nunca a nivel de persona.
- Trazabilidad de la fuente y separación entre datos abiertos y sintéticos.
- Reproducibilidad total del pipeline.
