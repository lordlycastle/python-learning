"""Tests for ``seed``, ``random_int``, ``random_number``, ``pick``, ``random_color``."""

from __future__ import annotations

import random as _stdlib_random

from firstpaint import (
    pick,
    random_color,
    random_int,
    random_number,
    seed,
)


class TestSeedReproducibility:
    def test_same_seed_gives_same_sequence(self):
        seed(42)
        a = [random_int(0, 100) for _ in range(10)]
        seed(42)
        b = [random_int(0, 100) for _ in range(10)]
        assert a == b

    def test_different_seeds_differ(self):
        seed(1)
        a = [random_int(0, 1000) for _ in range(20)]
        seed(2)
        b = [random_int(0, 1000) for _ in range(20)]
        assert a != b

    def test_seed_with_string_does_not_raise(self):
        seed("rainbow")  # type: ignore[arg-type]
        # And it should still be deterministic across calls.
        seed("rainbow")  # type: ignore[arg-type]
        a = [random_int(0, 100) for _ in range(5)]
        seed("rainbow")  # type: ignore[arg-type]
        b = [random_int(0, 100) for _ in range(5)]
        assert a == b


class TestIndependentOfStdlib:
    def test_firstpaint_seed_does_not_clobber_stdlib_random(self):
        # Pin stdlib, then disturb firstpaint, then check stdlib is undisturbed.
        _stdlib_random.seed(999)
        expected = [_stdlib_random.random() for _ in range(5)]

        _stdlib_random.seed(999)
        seed(1)
        random_int(0, 1000)
        random_number(0, 1)
        actual = [_stdlib_random.random() for _ in range(5)]

        assert actual == expected


class TestRandomInt:
    def test_bounds_inclusive(self):
        seed(0)
        for _ in range(200):
            v = random_int(5, 7)
            assert 5 <= v <= 7

    def test_swap_high_low(self):
        seed(0)
        v = random_int(100, 1)
        assert 1 <= v <= 100

    def test_low_equals_high(self):
        assert random_int(7, 7) == 7

    def test_junk_returns_zero(self):
        assert random_int("a", "b") == 0  # type: ignore[arg-type]


class TestRandomNumber:
    def test_default_range_is_zero_to_one(self):
        seed(0)
        for _ in range(200):
            v = random_number()
            assert 0.0 <= v < 1.0

    def test_custom_range(self):
        seed(0)
        for _ in range(200):
            v = random_number(10.0, 20.0)
            assert 10.0 <= v <= 20.0  # uniform is inclusive at top in practice

    def test_swap_high_low(self):
        seed(0)
        v = random_number(100.0, 1.0)
        assert 1.0 <= v <= 100.0

    def test_equal_bounds(self):
        assert random_number(5.0, 5.0) == 5.0


class TestPick:
    def test_picks_from_list(self):
        seed(0)
        chosen = pick(["a", "b", "c"])
        assert chosen in {"a", "b", "c"}

    def test_picks_from_tuple(self):
        seed(0)
        chosen = pick((1, 2, 3))
        assert chosen in {1, 2, 3}

    def test_empty_returns_none(self):
        assert pick([]) is None

    def test_pick_is_seedable(self):
        items = ["a", "b", "c", "d", "e"]
        seed(99)
        a = [pick(items) for _ in range(20)]
        seed(99)
        b = [pick(items) for _ in range(20)]
        assert a == b


class TestRandomColor:
    def test_returns_rgba_tuple(self):
        seed(0)
        c = random_color()
        assert isinstance(c, tuple)
        assert len(c) == 4

    def test_channels_in_range(self):
        seed(0)
        for _ in range(100):
            r, g, b, a = random_color()
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255
            assert a == 255

    def test_is_seedable(self):
        seed(7)
        a = [random_color() for _ in range(10)]
        seed(7)
        b = [random_color() for _ in range(10)]
        assert a == b

    def test_avoids_muddy_colors(self):
        """Colours should be reasonably saturated — at least one channel
        should usually be clearly bigger than another. A weak guarantee, but
        it catches a regression to pure random RGB."""
        seed(0)
        spreads = []
        for _ in range(50):
            r, g, b, _a = random_color()
            spreads.append(max(r, g, b) - min(r, g, b))
        # On HSV-derived colours with S>=0.65, the mean spread should be high.
        assert sum(spreads) / len(spreads) > 100
