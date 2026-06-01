"""Internal module-level state for the library.

This module is *not* part of the public vocabulary. It holds the current
canvas surface, current fill/stroke, and similar globals so the public
functions can stay parameter-light for learners (e.g. ``circle(x, y, r)``
rather than ``circle(surface, color, x, y, r)``).

The single-global model is a deliberate teaching choice (see CLAUDE.md §7).
Keep all mutable cross-module state in here so it's easy to find and reset
in tests.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Public RGB(A) type used in type hints across the library. Alpha is optional;
# when present, it ranges 0-255.
RGBA = tuple[int, int, int, int]


@dataclass
class _State:
    """Everything the library needs to remember between calls in one sketch."""

    # Drawing surface. ``None`` until ``canvas(...)`` (or a shape) initialises it.
    # Typed as ``object | None`` to avoid importing pygame at module load.
    surface: object | None = None

    # Canvas size as the learner sees it. Set by ``canvas(...)``.
    width: int = 600
    height: int = 600

    # Window title.
    title: str = "firstpaint"

    # Whether ``canvas(...)`` has actually been called (vs. defaults assumed).
    initialised: bool = False

    # Current fill / stroke. ``None`` means "do not draw this part".
    # Defaults match a Processing-style starter look: light-gray fill,
    # black 1px outline.
    fill_color: RGBA | None = field(default=(200, 200, 200, 255))
    stroke_color: RGBA | None = field(default=(0, 0, 0, 255))
    stroke_weight: int = 1


# Singleton. Tests can reset this via ``reset_state()``.
state = _State()


def reset_state() -> None:
    """Reset the global state in place. Used by tests; not part of the public API.

    Mutates fields on the existing singleton rather than rebinding the module
    global, so every module that did ``from ._state import state`` continues
    to observe the same object after a reset. Rebinding the global would leave
    those importers holding a stale reference.
    """
    fresh = _State()
    for field_name in fresh.__dataclass_fields__:
        setattr(state, field_name, getattr(fresh, field_name))
