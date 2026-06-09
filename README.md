# 🛡️ SecData Perú

## 🚀 GUÍA RÁPIDA PARA ABRIR EL PROYECTO

Para abrir y utilizar este tablero de seguridad en tu computadora, sigue estos pasos muy simples:

1. **Abre la carpeta del proyecto** en el explorador de archivos de Windows.
2. **Haz doble clic** en el archivo llamado **`iniciar-proyecto.bat`**.
3. **Espera unos segundos** a que se abra automáticamente tu navegador web con el tablero.
4. **Interactúa con el tablero** utilizando las pestañas superiores ("Resumen", "Mapa", "Tendencia", "Ranking", "Fuentes") y haz clic en las regiones.
5. **Cierra la ventana negra (terminal)** cuando termines.

---

**Tablero dinámico de seguridad ciudadana: hotspots de riesgo por región, alimentado con datos públicos y pensado para la toma de decisiones.**

> No es un mapa decorativo: es un **semáforo de riesgo** que ayuda a priorizar dónde concentrar patrullaje, presupuesto o intervención. Combina victimización, homicidios y percepción de inseguridad en un índice por región y permite recorrer su evolución en el tiempo.

![Vista previa del tablero de hotspots](docs/captura_dashboard.png)

🔗 **Página en vivo (GitHub Pages):** `https://oprbguitar.github.io/SecData-peru/`

---

## Declaración (encabezado de la página)

**Pierre R.** declara que los datos de esta página provienen de fuentes públicas y oficiales del Estado peruano —**INEI** (estadísticas de criminalidad y victimización) y el **Observatorio Nacional de Seguridad Ciudadana (OBNASEC – Ministerio del Interior)**—, trabajados de forma agregada por región. Se mencionan las fuentes sin necesidad de incluir enlaces.

📧 **Consultas adicionales:** [peru.labs.pe@gmail.com](mailto:peru.labs.pe@gmail.com)

---

## ¿De qué trata?

SecData Perú toma información **pública y agregada** de seguridad ciudadana y la convierte en un tablero único, claro y accionable. En lugar de revisar boletines sueltos, el usuario ve de un vistazo **qué regiones están peor, hacia dónde van y dónde actuar primero**.

La página interactiva incluye, además del tablero, secciones de texto que explican:

- **¿Qué es y para qué sirve?** — mapa de hotspots, línea de tiempo y enfoque de decisión.
- **Tablero interactivo** — mapa animado, KPIs, ranking y tendencia por región.
- **Cómo leer el índice de riesgo** — pesos del índice y significado del semáforo.
- **Próximos pasos: decidir con los datos** — ruta Detectar → Priorizar → Actuar → Evaluar y ejemplos de lectura para decisión.
- **Fuentes de los datos** — declaradas dentro de la propia página.

## Índice de riesgo (la lógica de decisión)

Cada región recibe un índice de **0 a 100** que combina, con pesos configurables:

- Tasa de victimización (45 %)
- Tasa de homicidios (35 %)
- Percepción de inseguridad (20 %)

Sobre ese resultado se aplica un **semáforo** (Alto / Medio / Bajo) para una lectura inmediata orientada a la priorización de recursos.

## Cómo está construido

```
Fuente pública ─► ingest ─► transform (índice + semáforo) ─► build_web ─► docs/data.json
                                                                  │
                                                                  ├─► docs/index.html  (GitHub Pages / local)
                                                                  └─► app/streamlit_app.py (local interactivo)
```

**Stack:** Python (pandas, numpy, requests, matplotlib) · Leaflet · Chart.js · Streamlit · GitHub Actions / Pages.

## Cómo ejecutarlo localmente

```bash
pip install -r requirements.txt

python -m src.run_pipeline            # genera los datos del tablero (modo muestra)
python -m src.run_pipeline --refresh  # intenta la fuente real configurada
python -m src.plot_preview            # imagen de vista previa

# Ver el tablero:
#   - dinámico:          abre docs/index.html (o publícalo en GitHub Pages)
#   - interactivo local: streamlit run app/streamlit_app.py
```

**Publicar la página:** en GitHub, *Settings → Pages → Source: rama `main`, carpeta `/docs`*. Queda disponible en `https://oprbguitar.github.io/SecData-peru/`.

**Actualización automática:** el flujo `.github/workflows/refresh.yml` ejecuta el pipeline de forma programada y vuelve a publicar el tablero.

## Limitaciones

- El mapa usa **centroides** de región (mapa de puntos); para coropletas exactas se puede añadir el límite geográfico oficial.
- Los umbrales del semáforo y los pesos del índice son **decisiones de política** y deben ajustarse al criterio de cada entidad.
- La victimización proviene de una encuesta (tiene margen de error); el índice es un **apoyo** a la decisión, no un veredicto.
- La muestra sintética sirve solo para demostración del funcionamiento.

## Confidencialidad

Proyecto **demostrativo**. Usa exclusivamente datos **públicos y agregados** y/o **sintéticos**. **No contiene información reservada, confidencial, datos personales ni información de empleadores actuales o anteriores.** Ver `docs/CONFIDENCIALIDAD.md`.

---

**Creado por Pierre R.** — Ingeniero Industrial · analítica institucional, geovisualización y automatización de datos.

📧 **Consultas adicionales:** [peru.labs.pe@gmail.com](mailto:peru.labs.pe@gmail.com)
