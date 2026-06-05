from pathlib import Path

from generators.planning_tools import generate_tools


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def write_nojekyll() -> None:
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    generate_tools()
    write_nojekyll()
