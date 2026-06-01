"""Canvas init + dimension publishing tests.

These use the dummy SDL driver so no real window opens.
"""

from __future__ import annotations

import firstpaint
from firstpaint import canvas
from firstpaint._state import state


class TestCanvasInit:
    def test_default_state_before_canvas(self):
        # _reset_state fixture has just run.
        assert state.surface is None
        assert state.initialised is False
        assert state.width == 600
        assert state.height == 600

    def test_canvas_sets_dimensions(self):
        canvas(800, 480)
        assert state.width == 800
        assert state.height == 480
        assert state.initialised is True
        assert state.surface is not None

    def test_canvas_publishes_to_package_namespace(self):
        canvas(320, 240)
        assert firstpaint.width == 320
        assert firstpaint.height == 240

    def test_canvas_clamps_too_small(self):
        canvas(0, -5)
        assert state.width == 1
        assert state.height == 1

    def test_canvas_clamps_too_large(self):
        canvas(99999, 99999)
        assert state.width == 4000
        assert state.height == 4000

    def test_canvas_default_size(self):
        canvas()
        assert state.width == 600
        assert state.height == 600

    def test_title_stored(self):
        canvas(200, 200, "hello world")
        assert state.title == "hello world"
