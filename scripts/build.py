#!/usr/bin/env python3
"""Build standalone executables with PyInstaller."""

from __future__ import annotations

import argparse
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
BUILD = ROOT / "build"
RELEASE = DIST / "release"
APP_NAME = "t7oolkit"


def get_version() -> str:
    init_file = SRC / "t7oolkit" / "__init__.py"
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_file.read_text())
    if not match:
        raise RuntimeError(f"Could not determine version from {init_file}")
    return match.group(1)


def get_platform_suffix() -> str:
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    return system


def clean() -> None:
    for path in (BUILD, DIST):
        if path.exists():
            shutil.rmtree(path)


def resolve_output(*, onefile: bool) -> Path:
    if platform.system() == "Darwin":
        return DIST / f"{APP_NAME}.app"

    if onefile:
        suffix = ".exe" if platform.system() == "Windows" else ""
        return DIST / f"{APP_NAME}{suffix}"

    if platform.system() == "Windows":
        return DIST / APP_NAME / f"{APP_NAME}.exe"

    return DIST / APP_NAME / APP_NAME


def run_pyinstaller(*, onefile: bool) -> Path:
    app_entry = SRC / "t7oolkit" / "app.py"
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(app_entry),
        "--name",
        APP_NAME,
        "--windowed",
        "--noconfirm",
        "--paths",
        str(SRC),
        "--distpath",
        str(DIST),
        "--workpath",
        str(BUILD / "pyinstaller"),
        "--specpath",
        str(BUILD),
        "--onedir" if not onefile else "--onefile",
    ]

    subprocess.run(cmd, check=True, cwd=ROOT)
    output = resolve_output(onefile=onefile)
    if not output.exists():
        raise FileNotFoundError(f"Expected build output not found: {output}")
    return output


def package_release(output: Path) -> Path:
    version = get_version()
    suffix = get_platform_suffix()
    RELEASE.mkdir(parents=True, exist_ok=True)
    archive_base = RELEASE / f"{APP_NAME}-{version}-{suffix}"

    if output.name.endswith(".app"):
        root_dir = output.parent
        base_dir = output.name
    elif output.is_dir():
        root_dir = output.parent
        base_dir = output.name
    else:
        root_dir = output.parent
        base_dir = output.name

    archive_path = shutil.make_archive(
        str(archive_base),
        "zip",
        root_dir=root_dir,
        base_dir=base_dir,
    )
    return Path(archive_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build t7oolkit standalone executable.")
    parser.add_argument("--clean", action="store_true", help="Remove build artifacts before building.")
    parser.add_argument("--onefile", action="store_true", help="Build a single executable file.")
    parser.add_argument(
        "--release",
        action="store_true",
        help="Create a release archive under dist/release/.",
    )
    args = parser.parse_args()

    if args.clean:
        clean()

    output = run_pyinstaller(onefile=args.onefile)
    print(f"Built: {output}")

    if args.release:
        archive = package_release(output)
        print(f"Release archive: {archive}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
