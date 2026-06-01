"""Test fixtures and global setup.

We force pygame's *dummy* video driver so tests never try to open a real
window — vital for CI and headless dev machines.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")


@pytest.fixture(autouse=True)
def _reset_state():
    """Reset firstpaint's module-level state between tests."""
    from firstpaint import _state

    _state.reset_state()
    yield
    _state.reset_state()
