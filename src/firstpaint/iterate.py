"""Iteration vocabulary: ``repeat`` and ``grid``.

Both are iterators — idiomatic Python and easier to teach than callbacks
(CLAUDE.md §7). A learner writes::

    for i in repeat(10):
        circle(i * 60 + 30, 300, 24)

    for cell in grid(6, 6):
        fill(random_color())
        circle(cell.center_x, cell.center_y, 26)
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from ._state import state
from .canvas import _ensure_canvas


def repeat(n: int) -> range:
    """Yield ``0, 1, ..., n - 1``. Negative or junk ``n`` becomes ``0``.

    ``for i in repeat(5)`` is the friendlier way to write ``for i in range(5)``.
    If a learner doesn't need the counter they can still write
    ``for _ in repeat(5): ...``.
    """
    try:
        count = int(n)
    except (TypeError, ValueError):
        return range(0)
    return range(count if count > 0 else 0)


@dataclass(frozen=True)
class Cell:
    """One cell of a ``grid(...)``.

    Attributes:
        col: column index, 0-based, growing right
        row: row index, 0-based, growing down
        x: top-left x of the cell, in pixels
        y: top-left y of the cell, in pixels
        width: cell width in pixels
        height: cell height in pixels
        center_x: x of the cell's centre, in pixels
        center_y: y of the cell's centre, in pixels
    """

    col: int
    row: int
    x: int
    y: int
    width: int
    height: int
    center_x: int
    center_y: int


def grid(cols: int, rows: int) -> Iterator[Cell]:
    """Split the canvas into ``cols × rows`` cells and yield each one.

    The order is row-major, top-to-bottom, left-to-right — the same order
    you'd read a page. ``cols`` and ``rows`` below 1 are clamped to 1.

    The canvas must already be sized for cell maths to make sense, so this
    auto-opens it with defaults if the learner forgot to call ``canvas(...)``.
    """
    try:
        c = int(cols)
    except (TypeError, ValueError):
        c = 1
    try:
        r = int(rows)
    except (TypeError, ValueError):
        r = 1
    if c < 1:
        c = 1
    if r < 1:
        r = 1

    _ensure_canvas()
    cell_w = max(1, state.width // c)
    cell_h = max(1, state.height // r)

    for row in range(r):
        for col in range(c):
            x = col * cell_w
            y = row * cell_h
            yield Cell(
                col=col,
                row=row,
                x=x,
                y=y,
                width=cell_w,
                height=cell_h,
                center_x=x + cell_w // 2,
                center_y=y + cell_h // 2,
            )
