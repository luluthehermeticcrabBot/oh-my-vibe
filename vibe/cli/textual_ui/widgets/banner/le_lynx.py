from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

# Original Oh My Vibe lynx artwork. Coordinates are braille dots, not copied
# from the former upstream cat animation.
WIDTH = 22
HEIGHT = 12
FRAME_INTERVAL_S = 0.24

_BASE = {
    1j + 6,
    1j + 7,
    1j + 14,
    1j + 15,
    2j + 5,
    2j + 8,
    2j + 13,
    2j + 16,
    3j + 4,
    3j + 9,
    3j + 12,
    3j + 17,
    4j + 4,
    4j + 8,
    4j + 13,
    4j + 17,
    5j + 5,
    5j + 6,
    5j + 7,
    5j + 14,
    5j + 15,
    5j + 16,
    6j + 6,
    6j + 15,
    7j + 7,
    7j + 8,
    7j + 13,
    7j + 14,
    8j + 8,
    8j + 13,
    9j + 9,
    9j + 10,
    9j + 11,
    9j + 12,
}

_EARS_HIGH = {0j + 5, 0j + 8, 0j + 13, 0j + 16}
_EARS_LOW = {1j + 5, 1j + 8, 1j + 13, 1j + 16}
_EYES_OPEN = {4j + 6, 4j + 15}
_EYES_CLOSED = {4j + 7, 4j + 14}

# A short, deliberately distinct motion: ear twitch, blink, then return.
_FRAMES = (
    _BASE | _EARS_HIGH | _EYES_OPEN,
    _BASE | _EARS_LOW | _EYES_OPEN,
    _BASE | _EARS_HIGH | _EYES_CLOSED,
    _BASE | _EARS_HIGH | _EYES_OPEN,
)


class LeLynx(Static):
    """Small original animated lynx used as Oh My Vibe's mascot."""

    def __init__(self, animate: bool = True, **kwargs: Any) -> None:
        classes = kwargs.pop("classes", None)
        merged_classes = "le-lynx" if classes is None else f"le-lynx {classes}"
        super().__init__(**kwargs, classes=merged_classes)
        self._animate_enabled = animate
        self._frame_index = 0
        self._timer: Timer | None = None
        self._freeze_requested = False

    def compose(self) -> ComposeResult:
        yield Static(self._frame(), classes="le-lynx-art")

    def on_mount(self) -> None:
        self._inner = self.query_one(".le-lynx-art", Static)
        if self._animate_enabled:
            self._timer = self.set_interval(FRAME_INTERVAL_S, self._next_frame)

    def freeze_animation(self) -> None:
        self._freeze_requested = True
        if self._timer:
            self._timer.stop()
            self._timer = None

    def _frame(self) -> str:
        return render_braille(_FRAMES[self._frame_index], WIDTH, HEIGHT)

    def _next_frame(self) -> None:
        if self._freeze_requested:
            return
        self._frame_index = (self._frame_index + 1) % len(_FRAMES)
        self._inner.update(self._frame(), layout=False)
