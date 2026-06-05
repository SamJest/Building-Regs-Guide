from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DATA_FOLDER = ROOT / "data"
TEMPLATES_FOLDER = ROOT / "templates"
OUTPUT_FOLDER = ROOT / "output"

BASE_URL = "https://ukplanningguide.co.uk"
FORCE_REBUILD = True
