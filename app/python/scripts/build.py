#!/usr/bin/env python3
"""Build standalone executables for the t7oolkit Python app with PyInstaller."""

from __future__ import annotations

import argparse
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
SRC = APP_ROOT / "src"
DIST = APP_ROOT / "dist"
BUILD = APP_ROOT / "build"
RELEASE = DIST / "release"
APP_NAME = "t7oolkit"
ENTRYPOINT = SRC / "t7oolkit" / "app.py"

HIDDEN_IMPORTS = (
    "PIL",
    "PIL.Image",
    "t7oolkit.config",
    "t7oolkit.registry.tool_registry",
    "t7oolkit.tools.demo_text_tool",
    "t7oolkit.tools.img_rect640_tool",
    "t7oolkit.tools.register",
    "t7oolkit.utils.image_resize",
)


def get_version() -> str:
    init_file = SRC / "t7oolkit" / "__init__.py"
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', init_file.read_text(encoding="utf-8"))
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


def run_command(cmd: list[str], *, cwd: Path = APP_ROOT) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=cwd)


def install_dependencies() -> None:
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements-build.txt"])
    run_command([sys.executable, "-m", "pip", "install", "-e", "."])


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
    if not ENTRYPOINT.exists():
        raise FileNotFoundError(f"Application entrypoint not found: {ENTRYPOINT}")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        str(ENTRYPOINT),
        "--name",
        APP_NAME,
        "--windowed",
        "--noconfirm",
        "--paths",
        str(SRC),
        "--collect-submodules",
        "t7oolkit",
        "--distpath",
        str(DIST),
        "--workpath",
        str(BUILD / "pyinstaller"),
        "--specpath",
        str(BUILD),
        "--onedir" if not onefile else "--onefile",
    ]

    for hidden_import in HIDDEN_IMPORTS:
        cmd.extend(["--hidden-import", hidden_import])

    run_command(cmd)
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
    parser = argparse.ArgumentParser(
        description="Build t7oolkit standalone executable from app/python/.",
    )
    parser.add_argument("--clean", action="store_true", help="Remove build artifacts before building.")
    parser.add_argument("--onefile", action="store_true", help="Build a single executable file.")
    parser.add_argument(
        "--release",
        action="store_true",
        help="Create a release archive under dist/release/.",
    )
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip installing runtime/build dependencies.",
    )
    args = parser.parse_args()

    if not args.skip_install:
        install_dependencies()

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
