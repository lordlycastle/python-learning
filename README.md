# firstpaint

Teach absolute beginners to program by drawing pictures.

This is the maintainer-facing README. Learner-facing docs live in
`curriculum/` (Phase 4).

## Status

**Parked until I teach again.**

Phases 0–4 are done: the library (static drawing, loops and randomness,
`animate`) runs on `pygame-ce`, and `curriculum/` holds the vocabulary and
task list. Phase 5 — the beginner install path — stopped at the decision
stage: PyCharm Core is locked as the IDE (`PHASE0.md` §C), but there is no
install guide, no "first sketch in five minutes" walkthrough, no clean-machine
test on Windows or macOS.

Why parked: no teaching for six months, and no evidence yet that learners
would adopt it.

**Re-check first on waking:** whether agentic coding tools have changed how
beginners learn to program. If a beginner's first program is now written with
an assistant, the modify-one-number approach and the Phase 5 install path may
need rethinking before any more work goes in.

See `CLAUDE.md` and `PHASE0.md` for the decisions behind every choice.

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
