"""
run_pipeline.py
-----------------
Lancia in sequenza l'intera pipeline:
  01_create_buffers -> 02_fetch_landuse -> 03_compute_percentages -> 04_export_kepler

Uso:
  python run_pipeline.py                    # tutti gli stadi (può richiedere tempo)
  python run_pipeline.py --priority-only     # solo Avellino + San Siro (consigliato per iniziare)
  python run_pipeline.py --stadium milano_san_siro
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"


def run(cmd):
    print(f"\n{'='*70}\n>>> {' '.join(cmd)}\n{'='*70}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(f"Errore nell'esecuzione di: {' '.join(cmd)}")


def main():
    parser = argparse.ArgumentParser(description="Esegue l'intera pipeline uso del suolo stadi.")
    parser.add_argument("--priority-only", action="store_true", help="Solo Avellino + San Siro")
    parser.add_argument("--stadium", type=str, help="ID di un singolo stadio")
    parser.add_argument("--no-html", action="store_true", help="Non generare la mappa HTML finale")
    args = parser.parse_args()

    py = sys.executable
    filter_args = []
    if args.stadium:
        filter_args = ["--stadium", args.stadium]
    elif args.priority_only:
        filter_args = ["--priority-only"]

    run([py, str(SCRIPTS_DIR / "01_create_buffers.py"), *filter_args])
    run([py, str(SCRIPTS_DIR / "02_fetch_landuse.py"), *filter_args])
    run([py, str(SCRIPTS_DIR / "03_compute_percentages.py")])  # opera su tutti i buffer già filtrati

    export_args = ["--no-html"] if args.no_html else []
    run([py, str(SCRIPTS_DIR / "04_export_kepler.py"), *export_args])

    print("\n✓ Pipeline completata. Output finale in data/output/stadi_landuse_kepler.geojson")


if __name__ == "__main__":
    main()
