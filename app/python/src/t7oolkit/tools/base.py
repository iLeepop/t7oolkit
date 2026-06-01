from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass

import tkinter.ttk as ttk


StatusCallback = Callable[[str], None]


@dataclass(frozen=True)
class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def entry(self, parent: ttk.Frame, *, on_status: StatusCallback) -> None:
        """Build tool UI inside parent and report status via on_status."""
