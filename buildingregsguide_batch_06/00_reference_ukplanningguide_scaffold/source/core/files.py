import os
import shutil


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_file(folder, filename, content):
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def copy_assets(src="assets", dest="output/assets"):
    if not os.path.exists(src):
        print("No assets folder found, skipping asset copy.")
        return

    if os.path.exists(dest):
        shutil.rmtree(dest)

    shutil.copytree(src, dest)
    print(f"Assets copied to {dest}")
