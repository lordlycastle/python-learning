"""Animation vocabulary: ``animate``, plus ``sin``, ``cos``, ``pi``.

``animate(draw)`` is the whole loop. The learner writes a ``draw(time)``
function that paints one frame; firstpaint owns the rest — the timing,
the buffer flip, the close-window event. This is the §7 mental model:

    def draw(time):
        background("#fdf6e3")
        circle(width / 2, height / 2, 20 + sin(time) * 12)

    animate(draw)

``time`` is **seconds since the sketch started**, as a float. So
``sin(time)`` smoothly wobbles between -1 and 1 once per ~6.28 seconds,
``sin(time * 2)`` wobbles twice as fast, and so on.

``sin``, ``cos`` and ``pi`` are re-exported from the standard library
``math`` module so a learner never has to write ``import math``. They take
radians (not degrees). That trade-off is intentional: a learner who meets
``pi`` once is better off than a learner who has to remember which version
of ``sin`` they're calling.
"""

from __future__ import annotations

import math as _math
from collections.abc import Callable

from . import _state
from .canvas import _ensure_canvas

# Re-exports. These are the same functions as ``math.sin`` etc. — no wrapping.
sin = _math.sin
cos = _math.cos
pi = _math.pi


DrawFn = Callable[[float], None]


def animate(draw: DrawFn, fps: int = 60, _frames: int | None = None) -> None:
    """Call ``draw(time)`` on a loop until the user closes the window.

    Arguments:
        draw: a function that takes one number — the seconds elapsed since
            the sketch started — and paints one frame.
        fps: target frames per second. Defaults to 60; clamped to at least 1.
        _frames: testing hook — if set, stop after this many frames. Not
            intended for learner use (hence the underscore).

    The loop owns the canvas: ``animate`` opens it with defaults if you
    haven't called ``canvas(...)`` yourself, ticks the frame clock, polls
    for the window close event, and quits cleanly when the user closes the
    window or when ``draw`` raises.

    If ``draw`` raises, the loop stops and the exception propagates — a
    learner's own bugs surface honestly. We only swallow the library's
    plumbing, never the learner's.
    """
    import pygame  # type: ignore[import-not-found]

    _ensure_canvas()

    target_fps = max(1, int(fps)) if isinstance(fps, (int, float)) else 60
    clock = pygame.time.Clock()
    start_ms = pygame.time.get_ticks()

    frames = 0
    running = True
    try:
        while running:
            # Check the test cap *before* calling draw so ``_frames=0``
            # short-circuits cleanly instead of running one frame first.
            if _frames is not None and frames >= _frames:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if not running:
                break

            elapsed = (pygame.time.get_ticks() - start_ms) / 1000.0
            draw(elapsed)
            pygame.display.flip()
            clock.tick(target_fps)
            frames += 1
    finally:
        if pygame.display.get_init():
            pygame.display.quit()
        # Reset state so a second sketch can run cleanly in the same process.
        _state.reset_state()
