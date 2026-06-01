from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


def _default_export_dir() -> str:
    downloads = Path.home() / "Downloads"
    if downloads.exists():
        return str(downloads)
    return str(Path.home())


def _config_path() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    else:
        base = Path.home() / ".config"
    return base / "t7oolkit" / "config.json"


@dataclass
class AppConfig:
    thread_count: int = 4
    export_dir: str = field(default_factory=_default_export_dir)

    @property
    def effective_export_dir(self) -> str:
        if self.export_dir.strip():
            return self.export_dir
        return _default_export_dir()

    @classmethod
    def load(cls) -> AppConfig:
        path = _config_path()
        if not path.exists():
            return cls()

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return cls()

        thread_count = data.get("thread_count", 4)
        export_dir = data.get("export_dir", _default_export_dir())
        return cls(
            thread_count=max(1, min(32, int(thread_count))),
            export_dir=str(export_dir),
        )

    def save(self) -> None:
        path = _config_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(asdict(self), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
