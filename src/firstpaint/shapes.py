"""Shape vocabulary: ``circle``, ``rect``, ``square``, ``line``, ``triangle``, ``text``.

Conventions a learner needs to know (these will live in ``VOCABULARY.md`` in
Phase 4):

* Coordinates are pixels. ``(0, 0)`` is the top-left of the canvas. ``x``
  grows to the right, ``y`` grows downward.
* For ``circle`` the ``(x, y)`` is the **centre** of the circle.
* For ``rect`` / ``square`` the ``(x, y)`` is the **top-left corner**.

Forgiving: negative sizes are clamped to 1. Bad colours fall back rather
than raise (see ``color._parse``). A shape with no fill and no stroke is a
no-op — drawing nothing is a valid result, not an error.
"""

from __future__ import annotations

from ._state import state
from .canvas import _ensure_canvas


def _min_size(n: float, lo: int = 1) -> int:
    """Clamp a size to at least ``lo`` so a typo doesn't make a shape vanish."""
    try:
        v = int(n)
    except (TypeError, ValueError):
        return lo
    return v if v >= lo else lo


def _coord(n: float) -> int:
    """Coerce a coordinate to int. Floats off-screen are fine — pygame clips."""
    try:
        return int(n)
    except (TypeError, ValueError):
        return 0


def _stroke_weight() -> int:
    return max(1, int(state.stroke_weight))


def circle(x: float, y: float, radius: float) -> None:
    """Draw a circle whose **centre** is at ``(x, y)`` with the given radius."""
    import pygame  # type: ignore[import-not-found]

    surface = _ensure_canvas()
    cx, cy = _coord(x), _coord(y)
    r = _min_size(radius)

    if state.fill_color is not None:
        pygame.draw.circle(surface, state.fill_color, (cx, cy), r, 0)
    if state.stroke_color is not None:
        pygame.draw.circle(surface, state.stroke_color, (cx, cy), r, _stroke_weight())


def rect(x: float, y: float, width: float, height: float) -> None:
    """Draw a rectangle whose **top-left corner** is at ``(x, y)``."""
    import pygame  # type: ignore[import-not-found]

    surface = _ensure_canvas()
    px, py = _coord(x), _coord(y)
    w = _min_size(width)
    h = _min_size(height)
    r = pygame.Rect(px, py, w, h)

    if state.fill_color is not None:
        pygame.draw.rect(surface, state.fill_color, r, 0)
    if state.stroke_color is not None:
        pygame.draw.rect(surface, state.stroke_color, r, _stroke_weight())


def square(x: float, y: float, size: float) -> None:
    """Draw a square — same as ``rect(x, y, size, size)``."""
    rect(x, y, size, size)


def line(x1: float, y1: float, x2: float, y2: float) -> None:
    """Draw a line from ``(x1, y1)`` to ``(x2, y2)`` in the current stroke colour."""
    import pygame  # type: ignore[import-not-found]

    if state.stroke_color is None:
        return  # a line with no stroke is invisible — quietly skip
    surface = _ensure_canvas()
    pygame.draw.line(
        surface,
        state.stroke_color,
        (_coord(x1), _coord(y1)),
        (_coord(x2), _coord(y2)),
        _stroke_weight(),
    )


def triangle(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
) -> None:
    """Draw a triangle from three corner points."""
    import pygame  # type: ignore[import-not-found]

    surface = _ensure_canvas()
    points = [
        (_coord(x1), _coord(y1)),
        (_coord(x2), _coord(y2)),
        (_coord(x3), _coord(y3)),
    ]
    if state.fill_color is not None:
        pygame.draw.polygon(surface, state.fill_color, points, 0)
    if state.stroke_color is not None:
        pygame.draw.polygon(surface, state.stroke_color, points, _stroke_weight())


def text(message: str, x: float, y: float, size: int = 20) -> None:
    """Draw ``message`` with its top-left at ``(x, y)``.

    The colour comes from the current ``fill`` (so to change text colour,
    call ``fill(...)`` before ``text(...)``). If fill is off, text is drawn
    in the stroke colour, then in black as a last resort — never invisible.
    """
    import pygame  # type: ignore[import-not-found]

    surface = _ensure_canvas()
    s = str(message)
    pt = max(1, int(size))

    color = state.fill_color or state.stroke_color or (0, 0, 0, 255)
    # SysFont(None, size) uses pygame's default; reliably available, no extra files.
    font = pygame.font.SysFont(None, pt)
    rendered = font.render(s, True, color[:3])
    surface.blit(rendered, (_coord(x), _coord(y)))
