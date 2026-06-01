"""Colour parser tests — non-visual logic only."""

from __future__ import annotations

from firstpaint._state import state
from firstpaint.color import _FALLBACK, _parse, fill, no_fill, no_stroke, stroke


class TestParseHex:
    def test_six_digit_hex_with_hash(self):
        assert _parse("#ff8800") == (255, 136, 0, 255)

    def test_six_digit_hex_without_hash(self):
        assert _parse("ff8800") == (255, 136, 0, 255)

    def test_three_digit_hex_expands(self):
        # #f80 -> #ff8800
        assert _parse("#f80") == (255, 136, 0, 255)

    def test_eight_digit_hex_includes_alpha(self):
        assert _parse("#ff880080") == (255, 136, 0, 128)

    def test_four_digit_hex_includes_alpha(self):
        # #f808 -> #ff880088
        assert _parse("#f808") == (255, 136, 0, 136)

    def test_case_insensitive(self):
        assert _parse("#FF8800") == _parse("#ff8800")


class TestParseTuple:
    def test_three_tuple(self):
        assert _parse((10, 20, 30)) == (10, 20, 30, 255)

    def test_four_tuple(self):
        assert _parse((10, 20, 30, 200)) == (10, 20, 30, 200)

    def test_channels_clamp_to_0_255(self):
        assert _parse((-50, 999, 128)) == (0, 255, 128, 255)


class TestParseInt:
    def test_int_makes_grey(self):
        assert _parse(128) == (128, 128, 128, 255)

    def test_zero_is_black(self):
        assert _parse(0) == (0, 0, 0, 255)

    def test_over_255_clamps_to_white(self):
        assert _parse(900) == (255, 255, 255, 255)


class TestParseNamed:
    def test_known_name(self):
        # pygame ships a colour-name table; "red" is reliable.
        r, g, b, _a = _parse("red")
        assert (r, g, b) == (255, 0, 0)

    def test_unknown_falls_back(self):
        assert _parse("notacolour") == _FALLBACK


class TestParseBadInput:
    def test_empty_string_falls_back(self):
        assert _parse("") == _FALLBACK

    def test_garbage_tuple_falls_back(self):
        # Two-element tuple is not a colour we recognise.
        assert _parse((1, 2)) == _FALLBACK  # type: ignore[arg-type]


class TestStateMutation:
    def test_fill_sets_state(self):
        fill("#112233")
        assert state.fill_color == (17, 34, 51, 255)

    def test_no_fill_clears(self):
        fill("red")
        no_fill()
        assert state.fill_color is None

    def test_stroke_sets_state(self):
        stroke((50, 60, 70))
        assert state.stroke_color == (50, 60, 70, 255)

    def test_no_stroke_clears(self):
        stroke("red")
        no_stroke()
        assert state.stroke_color is None
