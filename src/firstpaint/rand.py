"""Randomness vocabulary: ``seed``, ``random_int``, ``random_number``,
``pick``, ``random_color``.

The library owns its own ``random.Random`` instance. Calling ``seed(42)``
makes *firstpaint's* output reproducible without touching the standard
library's global ``random`` state — so a learner who later writes
``random.random()`` of their own isn't surprised when our seed silently
affects it.

Reproducibility is the first task in the curriculum (CLAUDE.md §7): same
seed, same picture. Don't break that contract without good reason.
"""

from __future__ import annotations

import colorsys
import random as _random_module
from collections.abc import Sequence
from typing import TypeVar

from ._state import RGBA

T = TypeVar("T")

# Private RNG instance. Tests reset this via ``_rng`` or call ``seed(...)``.
_rng = _random_module.Random()


def seed(n: int) -> None:
    """Set the random seed. With the same seed, you get the same picture every time.

    Pass any whole number. Non-integer input is coerced to an int where it
    can be, or ignored otherwise — a beginner's bad seed should never
    crash the sketch.
    """
    try:
        _rng.seed(int(n))
    except (TypeError, ValueError):
        # Fall back to seeding with a hash of the string representation so the
        # result is still deterministic for whatever the user passed.
        _rng.seed(hash(repr(n)))


def random_int(low: int, high: int) -> int:
    """Return a random whole number between ``low`` and ``high`` (both included).

    If ``low`` is bigger than ``high``, we swap them silently rather than
    raise — a learner who writes ``random_int(100, 1)`` still gets a number.
    """
    try:
        a = int(low)
        b = int(high)
    except (TypeError, ValueError):
        return 0
    if a > b:
        a, b = b, a
    return _rng.randint(a, b)


def random_number(low: float = 0.0, high: float = 1.0) -> float:
    """Return a random decimal number between ``low`` (inclusive) and ``high`` (exclusive).

    Defaults to the range 0–1 like the standard library's ``random()``.
    Swap-tolerant like ``random_int``.
    """
    try:
        a = float(low)
        b = float(high)
    except (TypeError, ValueError):
        return 0.0
    if a > b:
        a, b = b, a
    if a == b:
        return a
    return _rng.uniform(a, b)


def pick(items: Sequence[T]) -> T | None:
    """Pick one random item from a list (or any sequence).

    Returns ``None`` if the sequence is empty — a beginner who passes ``[]``
    should not see a traceback.
    """
    if not items:
        return None
    return _rng.choice(items)


def random_color() -> RGBA:
    """Return a random colour that's bright enough to actually see.

    We sample a hue uniformly and fix saturation + brightness high. Pure
    random RGB tends to produce muddy, low-contrast colours which look bad
    in a beginner's first grid; HSV-based randomness gives consistently
    pleasant output. The output is still a normal ``(r, g, b, a)`` tuple
    the rest of the library can pass to pygame unchanged.

    Locked design choice [Verified by owner review, 2026-06-25]:
        - Hue uniform across the full wheel.
        - Saturation in 0.65–0.90 (never washed out, never neon).
        - Value (brightness) in 0.80–0.95 (always readable on the off-white
          default background; never near-black).

        These bounds are part of the contract. ``random_color()`` is one
        of the first tasks in the curriculum — a beginner's "make this
        pretty" knob. Widening the bounds (or switching to RGB) would
        re-introduce the muddy-output failure mode it was tuned away from.
        Change only with a curriculum revision.
    """
    hue = _rng.random()
    saturation = 0.65 + _rng.random() * 0.25  # 0.65–0.90
    value = 0.80 + _rng.random() * 0.15  # 0.80–0.95
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    return (int(r * 255), int(g * 255), int(b * 255), 255)
