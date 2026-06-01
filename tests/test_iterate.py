"""Tests for ``repeat`` and ``grid``."""

from __future__ import annotations

from firstpaint import canvas, grid, repeat
from firstpaint.iterate import Cell


class TestRepeat:
    def test_yields_zero_to_n_minus_one(self):
        assert list(repeat(5)) == [0, 1, 2, 3, 4]

    def test_zero_yields_nothing(self):
        assert list(repeat(0)) == []

    def test_negative_yields_nothing(self):
        assert list(repeat(-3)) == []

    def test_float_is_coerced(self):
        assert list(repeat(3.7)) == [0, 1, 2]

    def test_junk_yields_nothing(self):
        assert list(repeat("nope")) == []  # type: ignore[arg-type]


class TestGridShape:
    def test_cell_count(self):
        canvas(600, 600)
        cells = list(grid(4, 3))
        assert len(cells) == 12

    def test_cell_order_is_row_major(self):
        canvas(600, 600)
        cells = list(grid(3, 2))
        coords = [(c.col, c.row) for c in cells]
        assert coords == [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)]

    def test_cell_dimensions_match_canvas(self):
        canvas(600, 400)
        cells = list(grid(6, 4))
        # Each cell should be 100 x 100.
        for c in cells:
            assert c.width == 100
            assert c.height == 100

    def test_cell_positions(self):
        canvas(600, 600)
        cells = list(grid(2, 2))
        # 300x300 cells starting at (0,0), (300,0), (0,300), (300,300).
        positions = sorted((c.x, c.y) for c in cells)
        assert positions == [(0, 0), (0, 300), (300, 0), (300, 300)]

    def test_cell_centers(self):
        canvas(600, 600)
        cells = list(grid(2, 2))
        centres = sorted((c.center_x, c.center_y) for c in cells)
        # Each 300x300 cell's centre is its top-left + 150.
        assert centres == [(150, 150), (150, 450), (450, 150), (450, 450)]

    def test_cell_is_immutable(self):
        canvas(600, 600)
        cell = next(iter(grid(2, 2)))
        assert isinstance(cell, Cell)
        # frozen dataclass — attribute assignment must raise
        try:
            cell.col = 99  # type: ignore[misc]
        except Exception:
            return
        raise AssertionError("Cell should be frozen")


class TestGridForgiving:
    def test_zero_cols_clamps_to_one(self):
        canvas(600, 600)
        cells = list(grid(0, 3))
        assert len(cells) == 3  # 1 col × 3 rows

    def test_negative_rows_clamps_to_one(self):
        canvas(600, 600)
        cells = list(grid(4, -2))
        assert len(cells) == 4  # 4 cols × 1 row

    def test_junk_input_clamps_to_one(self):
        canvas(600, 600)
        cells = list(grid("nope", "also nope"))  # type: ignore[arg-type]
        assert len(cells) == 1


class TestGridLazyCanvas:
    def test_grid_without_canvas_auto_opens(self):
        # No canvas() called — grid should still work with default dims.
        cells = list(grid(2, 2))
        assert len(cells) == 4
        # Default canvas is 600x600 → each cell is 300x300.
        assert all(c.width == 300 and c.height == 300 for c in cells)
