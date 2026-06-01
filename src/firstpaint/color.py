"""Colour vocabulary: ``fill``, ``no_fill``, ``stroke``, ``no_stroke``.

Forgiving by design (CLAUDE.md §7). A learner can pass:

* a hex string: ``"#fdf6e3"``, ``"#fff"``, ``"fdf6e3"``
* a CSS-ish name: ``"red"``, ``"steelblue"``, ``"hotpink"`` (pygame's name table)
* a 3-tuple of ints: ``(255, 100, 50)``
* a 4-tuple of ints (with alpha): ``(255, 100, 50, 180)``
* a single int 0-255 for a grey: ``128``

If the input is unrecognisable, we fall back to a visible default (magenta)
rather than raising — a beginner should still see *a* picture and notice the
oddity, not hit a traceback.
"""

from __future__ import annotations

from ._state import RGBA, state

# A bright, hard-to-miss fallback so bad colour input produces an obvious
# visual signal instead of an exception.
_FALLBACK: RGBA = (255, 0, 255, 255)

# A "color" in the public type sense — anything we know how to parse.
ColorLike = str | int | tuple[int, int, int] | tuple[int, int, int, int]


def _clamp_channel(v: int) -> int:
    """Clamp a channel value into 0-255 without raising."""
    if v < 0:
        return 0
    if v > 255:
        return 255
    return int(v)


def _parse_hex(s: str) -> RGBA | None:
    """Parse ``#rgb``, ``#rgba``, ``#rrggbb``, or ``#rrggbbaa`` (with or without ``#``)."""
    s = s.strip().lstrip("#")
    if not all(c in "0123456789abcdefABCDEF" for c in s):
        return None
    if len(s) == 3:
        r, g, b = (int(c * 2, 16) for c in s)
        return (r, g, b, 255)
    if len(s) == 4:
        r, g, b, a = (int(c * 2, 16) for c in s)
        return (r, g, b, a)
    if len(s) == 6:
        return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)
    if len(s) == 8:
        return (
            int(s[0:2], 16),
            int(s[2:4], 16),
            int(s[4:6], 16),
            int(s[6:8], 16),
        )
    return None


def _parse_named(s: str) -> RGBA | None:
    """Resolve a colour name using pygame's table. Returns ``None`` if unknown."""
    try:
        # Import lazily so the colour module can be imported (and unit-tested)
        # without a display.
        import pygame  # type: ignore[import-not-found]
    except Exception:  # pragma: no cover - pygame not installed
        return None
    try:
        c = pygame.Color(s)
    except (ValueError, TypeError):
        return None
    return (c.r, c.g, c.b, c.a)


def _parse(value: ColorLike) -> RGBA:
    """Convert any accepted colour input to an ``(r, g, b, a)`` 0-255 tuple.

    Always returns a colour. On unrecognised input, returns the fallback so
    learners get a visible result, not an error.
    """
    # int → grey
    if isinstance(value, bool):
        # bool is an int subclass; treat it as grey but explicitly to satisfy
        # the type checker and to be predictable.
        v = _clamp_channel(int(value) * 255)
        return (v, v, v, 255)
    if isinstance(value, int):
        v = _clamp_channel(value)
        return (v, v, v, 255)

    # tuple → rgb or rgba
    if isinstance(value, tuple):
        if len(value) == 3:
            r, g, b = value
            return (_clamp_channel(r), _clamp_channel(g), _clamp_channel(b), 255)
        if len(value) == 4:
            r, g, b, a = value
            return (
                _clamp_channel(r),
                _clamp_channel(g),
                _clamp_channel(b),
                _clamp_channel(a),
            )
        return _FALLBACK

    # string → hex or name
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return _FALLBACK
        if s.startswith("#") or all(c in "0123456789abcdefABCDEF" for c in s):
            parsed = _parse_hex(s)
            if parsed is not None:
                return parsed
        parsed = _parse_named(s)
        if parsed is not None:
            return parsed
        return _FALLBACK

    return _FALLBACK


def fill(color: ColorLike) -> None:
    """Set the colour used to *fill* shapes from now on."""
    state.fill_color = _parse(color)


def no_fill() -> None:
    """Stop filling shapes. Outlines (if any) still draw."""
    state.fill_color = None


def stroke(color: ColorLike) -> None:
    """Set the colour used to *outline* shapes from now on."""
    state.stroke_color = _parse(color)


def no_stroke() -> None:
    """Stop drawing outlines on shapes."""
    state.stroke_color = None
