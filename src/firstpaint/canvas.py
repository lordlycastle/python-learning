"""The canvas — window, surface, and the ``show()`` hold-the-window-open call.

Public vocabulary in this module:

* ``canvas(width, height, title)`` — open the drawing canvas
* ``background(color)`` — fill the entire canvas with a colour
* ``show()`` — keep the window open until the user closes it

The library *owns* the loop (CLAUDE.md §7). For static sketches in Phase 1,
``show()`` is the loop: it sits and waits for the close event. Phase 3 will
add ``animate(draw)`` for sketches that change over time.
"""

from __future__ import annotations

import sys

from . import _state
from ._state import state
from .color import ColorLike, _parse

# Default canvas size if a sketch never calls ``canvas(...)``. Picked to be
# square, not tiny, and not so big it overflows a laptop screen.
DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600
DEFAULT_TITLE = "firstpaint"

# Default background colour painted when the canvas first opens. A near-white
# off-white reads as "blank page" without being harsh.
_DEFAULT_BG: tuple[int, int, int, int] = (250, 248, 245, 255)


def _publish_dimensions(w: int, h: int) -> None:
    """Make ``width`` and ``height`` available as live ints in the user's namespace.

    A learner writes ``from firstpaint import *`` once at the top of their
    sketch. That binds ``width`` and ``height`` into their script's module
    globals at import-time. If they later call ``canvas(800, 600)``, we patch
    their globals so subsequent uses of ``width`` / ``height`` reflect the
    new size — matching the §7 mental model where ``circle(width / 2, ...)``
    just works.

    We update three places: the firstpaint package globals, the firstpaint
    submodule re-export point if any, and the immediate caller's globals.
    """
    # The firstpaint package itself (so future ``import firstpaint;
    # firstpaint.width`` reads correctly).
    pkg = sys.modules.get("firstpaint")
    if pkg is not None:
        setattr(pkg, "width", w)
        setattr(pkg, "height", h)

    # The caller's module globals (so a user who did ``from firstpaint import *``
    # before calling ``canvas`` sees the update).
    frame = sys._getframe(2) if hasattr(sys, "_getframe") else None  # _ensure_canvas → canvas → user
    if frame is not None:
        g = frame.f_globals
        # Only patch names the user actually bound — never inject new ones.
        if "width" in g:
            g["width"] = w
        if "height" in g:
            g["height"] = h


def _ensure_canvas() -> object:
    """Return a ready-to-draw surface, opening the canvas with defaults if needed.

    Called by every shape and ``background`` so a learner can write a 3-line
    sketch without an explicit ``canvas(...)`` call.
    """
    if state.surface is None:
        canvas(DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_TITLE)
    # state.surface is guaranteed non-None here; mypy/pyright happy with assert.
    assert state.surface is not None
    return state.surface


def canvas(
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
    title: str = DEFAULT_TITLE,
) -> None:
    """Open the drawing canvas. Call this once near the top of your sketch.

    Sizes below 1 are clamped to 1. Sizes above 4000 are clamped to 4000 so a
    stray zero doesn't shrink the window to nothing and a stray million doesn't
    crash the display.
    """
    import pygame  # type: ignore[import-not-found]

    w = max(1, min(4000, int(width)))
    h = max(1, min(4000, int(height)))

    # If we've already opened a window, just resize it. Re-init is fine in
    # SDL2 / pygame-ce but cheaper to set_mode again.
    if not state.initialised:
        pygame.display.init()
        pygame.font.init()

    state.surface = pygame.display.set_mode((w, h))
    pygame.display.set_caption(str(title))
    # Paint the default background so the canvas isn't full of stale OS memory.
    state.surface.fill(_DEFAULT_BG[:3])

    state.width = w
    state.height = h
    state.title = str(title)
    state.initialised = True

    _publish_dimensions(w, h)


def background(color: ColorLike) -> None:
    """Fill the entire canvas with one colour. Clears anything drawn so far."""
    surface = _ensure_canvas()
    rgba = _parse(color)
    # pygame's Surface.fill takes RGB(A); pass all four to honour alpha if the
    # surface supports it. Display surfaces ignore alpha but accept the tuple.
    surface.fill(rgba)  # type: ignore[attr-defined]


def show() -> None:
    """Show the canvas and keep it on screen until the user closes the window.

    For static sketches. Animated sketches use ``animate(draw)`` instead
    (coming in Phase 3).
    """
    import pygame  # type: ignore[import-not-found]

    _ensure_canvas()
    pygame.display.flip()

    # Headless / testing path: if there's no real display driver, ``show()``
    # should return immediately rather than block forever.
    driver = pygame.display.get_driver() if pygame.display.get_init() else None
    if driver == "dummy":
        return

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        pygame.time.wait(16)  # ~60Hz idle; we're not animating, just waiting

    pygame.display.quit()
    # Reset so a new sketch in the same Python process gets a fresh canvas.
    _state.reset_state()
