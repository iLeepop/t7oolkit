from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}


@dataclass(frozen=True)
class ResizeResult:
    filename: str
    source_size: tuple[int, int]
    output_size: tuple[int, int]
    skipped: bool = False


@dataclass(frozen=True)
class ResizeError:
    filename: str
    message: str


def list_image_files(input_dir: str | Path) -> list[Path]:
    directory = Path(input_dir)
    return sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def resize_image(input_path: str | Path, output_path: str | Path, max_size: int = 640) -> ResizeResult:
    """Resize image to fit within max_size x max_size while preserving aspect ratio."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(input_path) as img:
        source_size = (img.width, img.height)
        if img.width <= max_size and img.height <= max_size:
            img.save(output_path)
            return ResizeResult(
                filename=input_path.name,
                source_size=source_size,
                output_size=source_size,
                skipped=True,
            )

        ratio = min(max_size / img.width, max_size / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        resized = img.resize(new_size, Image.Resampling.LANCZOS)
        resized.save(output_path)
        return ResizeResult(
            filename=input_path.name,
            source_size=source_size,
            output_size=new_size,
        )


def batch_resize_images(
    input_dir: str | Path,
    output_dir: str | Path,
    *,
    max_size: int = 640,
    workers: int = 4,
) -> tuple[list[ResizeResult], list[ResizeError]]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = list_image_files(input_dir)
    if not files:
        return [], []

    results: list[ResizeResult] = []
    errors: list[ResizeError] = []

    def process(path: Path) -> ResizeResult | ResizeError:
        try:
            return resize_image(path, output_dir / path.name, max_size=max_size)
        except Exception as exc:
            return ResizeError(filename=path.name, message=str(exc))

    worker_count = max(1, min(workers, len(files)))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = {executor.submit(process, path): path for path in files}
        for future in as_completed(futures):
            outcome = future.result()
            if isinstance(outcome, ResizeError):
                errors.append(outcome)
            else:
                results.append(outcome)

    results.sort(key=lambda item: item.filename.lower())
    errors.sort(key=lambda item: item.filename.lower())
    return results, errors


def format_result_line(result: ResizeResult) -> str:
    if result.skipped:
        return f"{result.filename}: {result.source_size[0]}x{result.source_size[1]} (无需缩放)"
    return (
        f"{result.filename}: {result.source_size[0]}x{result.source_size[1]} "
        f"-> {result.output_size[0]}x{result.output_size[1]}"
    )
