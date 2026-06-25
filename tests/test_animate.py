"""Tests for ``animate``, ``sin``, ``cos``, ``pi``.

The animate loop runs against the dummy SDL driver (forced in conftest)
and uses the private ``_frames`` knob so the test terminates instead of
blocking on a QUIT event that will never arrive in headless mode.
"""

from __future__ import annotations

import math

import pytest

from firstpaint import animate, cos, pi, sin
from firstpaint._state import state


class TestTrigReexports:
    def test_sin_zero(self):
        assert sin(0) == 0.0

    def test_cos_zero(self):
        assert cos(0) == 1.0

    def test_pi_value(self):
        assert pi == math.pi

    def test_sin_is_math_sin(self):
        # We promised re-export, not a wrapper. If this ever changes the
        # learner-facing behaviour might still match math, but worth flagging.
        assert sin is math.sin
        assert cos is math.cos


class TestAnimateLoop:
    def test_runs_for_n_frames(self):
        calls: list[float] = []

        def draw(t: float) -> None:
            calls.append(t)

        animate(draw, fps=60, _frames=5)
        assert len(calls) == 5

    def test_zero_frames_calls_draw_zero_times(self):
        calls: list[float] = []

        def draw(t: float) -> None:
            calls.append(t)

        animate(draw, fps=60, _frames=0)
        assert len(calls) == 0

    def test_time_is_non_decreasing(self):
        seen: list[float] = []

        def draw(t: float) -> None:
            seen.append(t)

        animate(draw, fps=60, _frames=10)
        for a, b in zip(seen, seen[1:]):
            assert b >= a, f"time went backwards: {a} -> {b}"

    def test_time_starts_near_zero(self):
        seen: list[float] = []

        def draw(t: float) -> None:
            seen.append(t)

        animate(draw, fps=60, _frames=3)
        # First frame: roughly zero. Be generous — pygame init may take time.
        assert seen[0] < 0.5

    def test_auto_opens_canvas(self):
        # No explicit canvas() call. animate() should still produce a surface.
        def draw(t: float) -> None:
            pass

        assert state.surface is None
        animate(draw, fps=60, _frames=1)
        # Loop tears down in its finally clause and resets state, so we can't
        # observe state.surface after — but reaching this line without raising
        # is sufficient evidence the canvas opened.

    def test_state_is_reset_after_loop(self):
        def draw(t: float) -> None:
            pass

        animate(draw, fps=60, _frames=1)
        assert state.surface is None
        assert state.initialised is False


class TestAnimateEscape:
    def test_escape_key_stops_loop(self):
        import pygame

        calls: list[float] = []

        def draw(t: float) -> None:
            calls.append(t)
            # On the 2nd frame, post Esc. The event will be drained at the
            # top of the *next* iteration, so the loop exits before draw is
            # called a 3rd time.
            if len(calls) == 2:
                pygame.event.post(
                    pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
                )

        animate(draw, fps=60, _frames=10)
        assert len(calls) == 2

    def test_non_escape_keydown_does_not_stop_loop(self):
        import pygame

        calls: list[float] = []

        def draw(t: float) -> None:
            calls.append(t)
            if len(calls) == 1:
                # Some other key — must not terminate the loop.
                pygame.event.post(
                    pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                )

        animate(draw, fps=60, _frames=4)
        assert len(calls) == 4


class TestAnimateForgiving:
    def test_fps_clamps_to_at_least_one(self):
        def draw(t: float) -> None:
            pass

        animate(draw, fps=0, _frames=1)  # no crash

    def test_negative_fps_clamps(self):
        def draw(t: float) -> None:
            pass

        animate(draw, fps=-30, _frames=1)


class TestAnimateErrorPropagation:
    def test_exception_in_draw_propagates(self):
        def draw(t: float) -> None:
            raise ValueError("learner's bug")

        with pytest.raises(ValueError, match="learner's bug"):
            animate(draw, fps=60, _frames=5)

    def test_exception_still_resets_state(self):
        def draw(t: float) -> None:
            raise RuntimeError("boom")

        with pytest.raises(RuntimeError):
            animate(draw, fps=60, _frames=5)
        # The finally clause must have run, leaving state clean.
        assert state.surface is None
        assert state.initialised is False
