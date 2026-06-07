"""firstpaint — the entire learner-facing vocabulary lives here.

A learner writes::

    from firstpaint import *

…and from that one line gets the whole world of names they'll need.
Internal module boundaries (``canvas``, ``shapes``, ``color``) exist for the
maintainers; the learner never sees them.

Phase 1 vocabulary (CLAUDE.md §9): canvas, shapes, color. No animation, no
randomness, no loops yet — those come in Phases 2 and 3.
"""

from __future__ import annotations

from .animate import animate, cos, pi, sin
from .canvas import DEFAULT_HEIGHT as _DEFAULT_HEIGHT
from .canvas import DEFAULT_WIDTH as _DEFAULT_WIDTH
from .canvas import background, canvas, show
from .color import fill, no_fill, no_stroke, stroke
from .iterate import Cell, grid, repeat
from .rand import pick, random_color, random_int, random_number, seed
from .shapes import circle, line, rect, square, text, triangle

# Live canvas size. These mirror ``canvas(...)``'s arguments so a learner can
# write ``circle(width / 2, height / 2, 50)``. They are updated whenever
# ``canvas(...)`` is called (including the lazy default opening). See
# ``canvas._publish_dimensions`` for the patching logic.
width: int = _DEFAULT_WIDTH
height: int = _DEFAULT_HEIGHT

__version__ = "0.1.0"

# The flat vocabulary `from firstpaint import *` pulls in. Keep this in lockstep
# with curriculum/VOCABULARY.md when it's written in Phase 4.
__all__ = [
    # canvas
    "canvas",
    "background",
    "show",
    "width",
    "height",
    # colour
    "fill",
    "no_fill",
    "stroke",
    "no_stroke",
    # shapes
    "circle",
    "rect",
    "square",
    "line",
    "triangle",
    "text",
    # iteration
    "repeat",
    "grid",
    "Cell",
    # randomness
    "seed",
    "random_int",
    "random_number",
    "pick",
    "random_color",
    # animation
    "animate",
    "sin",
    "cos",
    "pi",
]
