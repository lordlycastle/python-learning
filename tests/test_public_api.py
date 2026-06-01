"""Smoke test the public ``from firstpaint import *`` surface.

This is the only contract a learner sees. If it changes, the learner-facing
vocabulary has changed — which should be a deliberate decision, not an
accident.
"""

from __future__ import annotations

import firstpaint


def test_all_lists_phase_1_vocabulary():
    expected = {
        "canvas",
        "background",
        "show",
        "width",
        "height",
        "fill",
        "no_fill",
        "stroke",
        "no_stroke",
        "circle",
        "rect",
        "square",
        "line",
        "triangle",
        "text",
    }
    assert set(firstpaint.__all__) == expected


def test_star_import_binds_every_name():
    # Simulate what `from firstpaint import *` does, without actually polluting
    # the test module's globals.
    ns: dict[str, object] = {}
    exec("from firstpaint import *", ns)
    for name in firstpaint.__all__:
        assert name in ns, f"{name} missing from star-import"
