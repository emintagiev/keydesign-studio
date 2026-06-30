#!/usr/bin/env python3
"""Собрать полный сайт для отправки в Telegram (папка + ZIP)."""

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FOLDER_NAME = "Key Design Studio"
OUTPUT = Path.home() / "Desktop" / FOLDER_NAME
ZIP_PATH = Path.home() / "Desktop" / "Key-Design-Studio.zip"

SITE_FILES = [
    "index.html",
    "key-design-studio.html",
    "about.html",
    "projects.html",
    "approach.html",
    "partners.html",
    "dream-house.html",
    "zhk-pulsar.html",
    "moscow-studio.html",
    "salok-krasoty-tati.html",
    "laki-park-dom.html",
    "zhk-arkhitektor.html",
    "ns-akadem-pulsar.html",
    "kvartal-dekabristov.html",
    "nevskaya-dom.html",
    "vostochny-vayb.html",
    "kedrovy-ns.html",
    "kabinet-morozovo.html",
    "styles.css",
    "app.js",
    "project.js",
    "brief-config.js",
]

SKIP_HTML = {"preview.html"}


def patch_html(text: str) -> str:
    return re.sub(r"\?v=\d+", "", text)


def write_readme():
    (OUTPUT / "КАК ОТКРЫТЬ.txt").write_text(
        "Key Design Studio - сайт для просмотра\n\n"
        "=== iPhone / iPad (Apple) ===\n"
        "1. В Telegram нажмите на файл Key-Design-Studio.zip\n"
        "2. «Поделиться» → «Сохранить в Файлы» (выберите папку «Загрузки»)\n"
        "3. Откройте приложение «Файлы» → найдите архив\n"
        "4. Нажмите на zip - появится папка «Key Design Studio»\n"
        "5. Зайдите в папку и нажмите index.html\n"
        "6. Сайт откроется в Safari со всеми страницами и фото\n\n"
        "=== Mac / Windows ===\n"
        "Распакуйте zip, откройте index.html двойным кликом.\n\n"
        "Важно: отправляйте именно ZIP-архив, не один HTML-файл.\n",
        encoding="utf-8",
    )


def main():
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)

    shutil.copytree(ROOT / "assets", OUTPUT / "assets")

    for name in SITE_FILES:
        src = ROOT / name
        if not src.exists():
            raise SystemExit(f"Missing: {name}")
        if name.endswith(".html"):
            (OUTPUT / name).write_text(patch_html(src.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copy2(src, OUTPUT / name)

    write_readme()

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in sorted(OUTPUT.rglob("*")):
            if path.is_file():
                arc = Path(FOLDER_NAME) / path.relative_to(OUTPUT)
                zf.write(path, arc)

    size_mb = ZIP_PATH.stat().st_size / 1024 / 1024
    print(f"Folder: {OUTPUT}")
    print(f"ZIP:    {ZIP_PATH} ({size_mb:.1f} MB)")
    print("\nОтправьте в Telegram файл Key-Design-Studio.zip с Рабочего стола.")


if __name__ == "__main__":
    main()
