"""
run_pipeline.py — Flujo completo: ingesta -> indicadores -> tablero web.

    python -m src.run_pipeline             # offline (muestra)
    python -m src.run_pipeline --refresh   # intenta fuente real (INEI/datos abiertos)
"""
import argparse

from src import ingest, transform, build_web


def main(refresh=False):
    print("=" * 60)
    print("SeguridadData Perú — pipeline")
    print("=" * 60)
    crudo = ingest.ingestar(refresh=refresh)
    transform.transformar(crudo)
    build_web.construir()
    print("\nListo. Abre docs/index.html (o publícalo en GitHub Pages) y/o ejecuta:")
    print("   streamlit run app/streamlit_app.py")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    main(refresh=ap.parse_args().refresh)
