"""Shape input-handling tests — clamping and lazy-canvas behaviour.

We don't pixel-check the visual output; we check that shapes accept
beginner-hostile inputs (negatives, zero, junk) without raising and that the
state side-effects are right.
"""

from __future__ import annotations

from firstpaint import (
    canvas,
    circle,
    fill,
    line,
    no_fill,
    no_stroke,
    rect,
    square,
    stroke,
    text,
    triangle,
)
from firstpaint._state import state


class TestLazyInit:
    def test_circle_without_canvas_opens_default(self):
        # No canvas() call. The shape should auto-open the canvas.
        circle(100, 100, 20)
        assert state.initialised is True
        assert state.width == 600 and state.height == 600


class TestForgivingInputs:
    def test_negative_radius_does_not_raise(self):
        canvas(400, 400)
        circle(100, 100, -50)

    def test_zero_radius_does_not_raise(self):
        canvas(400, 400)
        circle(100, 100, 0)

    def test_negative_rect_does_not_raise(self):
        canvas(400, 400)
        rect(50, 50, -10, -10)

    def test_square_with_negative_size_does_not_raise(self):
        canvas(400, 400)
        square(20, 20, -5)

    def test_triangle_handles_offscreen_points(self):
        canvas(400, 400)
        triangle(-100, -100, 999, 50, 200, 999)

    def test_line_with_no_stroke_is_silent_noop(self):
        canvas(400, 400)
        no_stroke()
        line(0, 0, 100, 100)  # nothing to draw — must not raise

    def test_text_handles_non_string(self):
        canvas(400, 400)
        text(42, 10, 10)  # type: ignore[arg-type]
        text(3.14, 10, 30)  # type: ignore[arg-type]


class TestFillStrokeInteraction:
    def test_circle_with_neither_fill_nor_stroke_is_noop(self):
        canvas(400, 400)
        no_fill()
        no_stroke()
        circle(100, 100, 30)  # must not raise

    def test_fill_only(self):
        canvas(400, 400)
        fill("red")
        no_stroke()
        circle(100, 100, 30)

    def test_stroke_only(self):
        canvas(400, 400)
        no_fill()
        stroke("blue")
        circle(100, 100, 30)
