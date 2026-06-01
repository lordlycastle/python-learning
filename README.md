# firstpaint

Teach absolute beginners to program by drawing pictures.

This is the maintainer-facing README. Learner-facing docs live in
`curriculum/` (Phase 4).

## Status

Phase 1: core static drawing (canvas, shapes, color) on `pygame-ce`. No
animation yet — that's Phase 3. See `CLAUDE.md` and `PHASE0.md` for the
decisions behind every choice.

## Quick check (developer)

```bash
uv sync
uv run pytest
uv run python examples/sun.py
```

## What a learner writes

```python
from firstpaint import *

canvas(600, 600)
background("#fdf6e3")

fill("#e67e22")
no_stroke()
circle(300, 300, 120)

show()
```
