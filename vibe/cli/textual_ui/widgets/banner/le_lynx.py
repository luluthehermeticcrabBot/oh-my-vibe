from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.timer import Timer
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.braille_renderer import render_braille

# Original Oh My Vibe lynx artwork. This is deliberately a whole-body,
# side-on silhouette: tall ear tufts, cheek ruff, spotted-looking face,
# compact tail, long legs, and paws are all retained at terminal size.
WIDTH = 36
HEIGHT = 29
FRAME_INTERVAL_S = 0.24

# Dot-grid artwork: two columns of dots per braille cell and four rows per cell.
# Keeping the source as a readable silhouette makes future mascot edits safer.
_BASE_ART = (
    "        ##       ##                 ",
    "       ####     ####                ",
    "       ####     ####                ",
    "      ##  ##   ##  ##               ",
    "      ##  ##   ##  ##               ",
    "     ##################             ",
    "    ####################            ",
    "   #######  ####  #######           ",
    "   ######    ##    ######           ",
    "   ######################           ",
    "    ####################            ",
    "     ####  ########  ####           ",
    "      ##################            ",
    "       ################             ",
    "      #######################       ",
    "    #########################       ",
    "   ##########################  ##   ",
    "  ####### ################ ### ###  ",
    "  ####### ################ ###  ##  ",
    "  ############################  ##  ",
    "   ##########################    #  ",
    "    ######  ######  ######         ",
    "    ######  ######  ######         ",
    "    ######  ######  ######         ",
    "    ######  ######  ######         ",
    "   ######   ######   ######        ",
    "   ######   ######   ######        ",
    "    ####     ####     ####         ",
    "    ####     ####     ####         ",
)


def _dots(rows: tuple[str, ...]) -> frozenset[complex]:
    return frozenset(
        complex(x, y)
        for y, row in enumerate(rows)
        for x, char in enumerate(row)
        if char == "#"
    )


_BASE = _dots(_BASE_ART)

# The animation stays readable: the ear tufts twitch and the lynx blinks.
_EAR_TWITCH = _BASE - {complex(8, 0), complex(17, 0)} | {complex(7, 0), complex(18, 0)}
_EYES_BLINK = _BASE - {complex(8, 7), complex(15, 7)}

_FRAMES = (_BASE, _EAR_TWITCH, _EYES_BLINK, _BASE)


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
