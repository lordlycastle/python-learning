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

import pathlib
import sys

from . import _state
from ._state import state
from .color import ColorLike, _parse

# Used by ``_publish_dimensions`` to identify firstpaint's own frames so
# they can be skipped when walking up the call stack to find user code.
_PKG_PATH = pathlib.Path(__file__).resolve().parent

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

    We update two places: the firstpaint package globals, and the first
    user-code frame found by walking up the call stack. The frame walk
    skips any frames inside the firstpaint package itself, so the trick
    survives indirection — whether the user called ``canvas(...)``
    directly, or it was opened lazily through ``_ensure_canvas`` from
    inside ``animate``, the same user frame still gets patched.

    Why this exists (do not rip out without reading §7):
        The two alternatives are both worse for a beginner:

        1. Expose ``firstpaint.width`` / ``firstpaint.height`` and tell the
           learner to write ``circle(firstpaint.width / 2, ...)``. That
           forces a *namespace* concept on someone who hasn't met modules
           yet, and it breaks the ``from firstpaint import *`` promise that
           the library is one flat vocabulary.

        2. Make ``width`` and ``height`` functions instead of names —
           ``circle(width() / 2, ...)``. That adds parentheses that mean
           nothing to a learner, and inverts how every other dimension
           number in the rest of the curriculum is written.

        Patching globals is mildly magical, but the magic stays invisible
        to the learner — which is exactly the §3 trade-off the project
        opts into. Internal plumbing is allowed to be clever so long as
        the surface stays plain.
    """
    # 1. The firstpaint package itself (so ``firstpaint.width`` reads correctly).
    pkg = sys.modules.get("firstpaint")
    if pkg is not None:
        pkg.width = w  # type: ignore[attr-defined]
        pkg.height = h  # type: ignore[attr-defined]

    # 2. The first non-firstpaint frame above us — that's the user.
    if not hasattr(sys, "_getframe"):
        return

    pkg_dir = str(_PKG_PATH)
    frame = sys._getframe(1)
    while frame is not None:
        filename = frame.f_code.co_filename or ""
        # Skip frames whose code lives inside the firstpaint package.
        if not filename.startswith(pkg_dir):
            g = frame.f_globals
            # Only patch names the user actually bound — never inject new ones.
            if "width" in g:
                g["width"] = w
            if "height" in g:
                g["height"] = h
            return
        frame = frame.f_back


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
