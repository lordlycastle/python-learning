# CLAUDE.md — firstpaint

> **What this file is:** the seed instructions for the agent(s) building this
> repository. It records *decisions and their reasoning* so you don't
> re-litigate settled choices or fabricate around open ones. Read it fully
> before writing code. When this file and your training instinct disagree,
> this file wins; when this file is silent or marked **[Open]**, you **ask the
> owner** — you do not guess.

---

## 0. Operating contract (how you, the agent, must behave)

These rules are non-negotiable and apply to every action in this repo:

- **Do not fabricate.** Never invent package names, versions, APIs, functions,
  file paths, or citations. If you need a fact about a third-party package
  (does it exist, what's the current version, does it still require Java, is
  the PyPI name free), **verify it from a live source** — do not trust memory,
  which may be stale.
- **Distinguish confidence explicitly**, using the legend in §1. Tag claims you
  add to docs or PRs the same way.
- **Ask before proceeding on anything marked [Open]** or anything genuinely
  ambiguous. Surface a short, specific question; do not silently pick.
- **Verify-then-build.** Anything depending on a third-party package's current
  state goes through Phase 0 (§9) first. No drawing code is written against a
  substrate until the substrate is confirmed (§5.1).
- **Be direct in PRs and notes.** No filler. State what you did, what you
  assumed, and what you could not verify.
- **Build the smallest thing that works.** This is a low-complexity project for
  a tiny audience. Queues, plugin systems, async, microservices, abstract base
  hierarchies — all out of scope unless the owner asks. See §10.

---

## 1. Confidence legend

Use these tags in this file, in docs, and in PR descriptions:

- **[Verified]** — confirmed from a live source this session, or established fact.
- **[Inference]** — reasoning that is probably right, not confirmed.
- **[Assumption]** — a working default chosen to make progress; flag it so it
  can be overridden.
- **[Open]** — an unresolved decision the owner must make. **Do not resolve it
  yourself.**

---

## 2. Mission

Build a native-Python library (and, later, a small body of curriculum) that
teaches absolute beginners to program **through visual output**. A learner
writes a few lines, a picture appears; they change one number, the picture
changes. The draw is to *modify* code, not just run it.

The expensive, reusable asset of this project is **the teaching design** — the
API vocabulary and the task sequence — not the rendering plumbing. Protect that
design discipline (§7) above all.

This project is the Python sibling of an earlier browser/TypeScript playground.
**Do not try to replicate the browser version or share code with it.** Only the
*philosophy* and the *vocabulary* carry over. We are optimising for native
Python's strengths, not porting a web app.

---

## 3. The learner (anchor every decision to this person)

- Has **no prior technological experience.** Has likely never used a terminal,
  installed software for development, or seen a stack trace.
- Will be **demoralised by setup friction.** Their first experience must be a
  shape on screen, not a `PATH` error. This is the single biggest risk to the
  whole project (§9, Phase 5).
- Should **never need to read engineering-style docs** (single-responsibility,
  class hierarchies, lifecycle diagrams). The in-repo learner docs are a flat
  vocabulary list and a task list — nothing more.
- Is heading toward **real Python**. Everything they touch should be genuine,
  transferable Python (real functions, real errors, real packages), with the
  ceremony hidden, not faked.

---

## 4. Decisions already made — **[Locked]**, with reasoning

Do not reopen these without the owner.

| Decision | Choice | Reasoning |
|---|---|---|
| Language | **Native Python only** | A Python-only course. Optimise the long arc (real language, real ecosystem, transferable skills) over first-five-minutes convenience. |
| What we replicate from the prior project | **Philosophy + vocabulary only** | The curriculum is the asset; the code is not. No shared code, no web concepts. |
| API character | **One meaningful function each** | See §7. Optimise for "a beginner can read the line aloud and picture it," not for engineering separation of concerns. |
| Failure posture | **Forgiving over strict** | Bad inputs clamp/default to *something visible*; they do not raise. The learner should always see a result, then wonder why. |
| Loop ceremony | **Hidden behind the library** | The learner never writes an event loop or a `while True`. The library owns it; `animate(draw)` exposes it as one function. |
| Type hints | **Public API is fully type-hinted** | So learners on a checker-capable editor get real feedback; harmless to those who aren't. Hints are gradual, never enforced on learner code. |

---

## 5. Open decisions — **[Open]**, do not resolve alone

These block parts of the plan. Surface each to the owner with a crisp
recommendation; wait for the call.

### 5.1 Rendering substrate — **the most consequential open decision**

The substrate determines performance, the install story, and the mental-model
fit. **Phase 0 (§9) verifies the current state of each before any commitment.**

Recommended default, pending verification: **`pygame` / `pygame-ce`**.
[Inference] Best fit for the immediate-mode, animated, interactive feel; fast
enough for dense/animated sketches; its event-loop boilerplate is exactly what
the library will hide. Cost: a pip install and a real dependency.

Alternatives to weigh in the Phase 0 report:

- **`turtle` / `tkinter` (standard library).** Zero install, ships with
  CPython. But retained-mode (mismatched with our immediate-mode model) and
  slow at density — hits a wall at animation. [Inference] Good only if avoiding
  any pip install is judged worth capping capability.
- **`py5` / Processing-for-Python.** Cleanest immediate-mode/Processing model,
  but **[Verify]** whether it still requires a JDK — a heavy dependency for
  this audience. Likely disqualifying for absolute beginners unless that has
  changed.
- **Jupyter + `ipycanvas`.** Inline output, cell-level instant feedback, lower
  terminal friction. But adds Jupyter setup, limited animation, and teaches a
  non-standard execution model (out-of-order cells, hidden state) that can
  instil habits we'd later have to un-teach.

Do **not** write drawing code until this is confirmed.

### 5.2 Scope: library vs. platform

The owner described this as "app/lib/platform." Treat scope as **layered**, and
get explicit sign-off before planning any layer beyond the first:

1. **Core library** (the solid foundation — build this first regardless).
2. **Curriculum** (the task sequence + a flat learner doc).
3. **Delivery/platform** (a lesson runner, progress tracking, hosting,
   classroom features). **[Open]** — undefined and possibly out of scope.
   Do not design or build this until the owner defines what "platform" means.

### 5.3 Package / import name — **[Locked]** as `firstpaint`

- **Project name:** `firstpaint`
- **Distribution name on PyPI:** `firstpaint`
- **Import:** `from firstpaint import *`
- **Resolved:** 2026-05-31 by the owner, after Phase 0 verified that single-word
  abstract names on PyPI are squat-saturated and that `firstpaint` /
  `first-paint` / `first_paint` (all PEP 503 equivalents) returned no project
  page on this date. [Verified-available-as-of-2026-05-31]
- **Reasoning:** compound name (the modern ecosystem standard — `numpy`,
  `streamlit`, `manim`); signals the audience without being patronising; reads
  as a verb that hints at the act; matches `pip install firstpaint` →
  `from firstpaint import *` (one word for the learner). Earlier working name
  "Visual Python" was dropped because `visualpython` is an active GPLv3
  Jupyter extension on PyPI — direct identity collision.
- **Before first publish:** re-verify availability via a real registration
  attempt; PEP 541 doesn't apply since no slot is held.

### 5.4 Beginner environment / IDE target

The onboarding strategy (Thonny, a pre-built environment, a one-command
installer, a managed classroom setup) is **[Open]** and is the make-or-break
factor (§3, §9 Phase 5). Recommend, don't assume.

---

## 6. Repo structure — **[Recommended]**, adjust as the build teaches you

Keep it flat and obvious. A learner who opens the repo should not be lost.

```
/
  README.md              # for the instructor/maintainer (not the learner)
  CLAUDE.md              # this file
  pyproject.toml         # packaging, deps, tool config (type checker, formatter, tests)
  src/firstpaint/        # the library (§5.3)
    __init__.py          # re-exports the public vocabulary; this IS the API surface
    canvas.py            # window + draw surface + the hidden loop
    shapes.py            # circle, rect, square, line, triangle, text
    color.py             # fill, no_fill, stroke, no_stroke
    iterate.py           # repeat, grid (grid yields cells — see §7)
    rand.py              # seed, random_*, pick, random_color
    animate.py           # animate(draw): owns the frame loop
  examples/              # runnable sketches, one concept each
  curriculum/            # the task sequence (built in Phase 4)
    VOCABULARY.md        # the entire flat API list a learner ever needs
    TASKS.md             # numbered modify-this tasks, each tagged with its concept
  tests/                 # see §8
```

The public vocabulary lives behind `__init__.py` so the learner's whole world is
`from firstpaint import *`. Internal module boundaries are for *you*; they are
never exposed to the learner and never appear in learner docs.

---

## 7. Teaching-API design rules (the heart of the project — do not violate)

Every public function must pass this test: **can a beginner read the call aloud
and picture what appears?** Concretely:

- **One meaningful function each.** `circle(x, y, radius)` draws a circle.
  Not a `Shape` factory, not a builder, not a config object. If you find
  yourself adding a class hierarchy or an options dict to a learner-facing call,
  stop — that's the engineering instinct this project explicitly rejects.
- **Snake_case, plain words.** `random_color`, `no_fill`. Names are verbs or
  nouns a non-programmer knows.
- **Forgiving.** Negative or nonsensical sizes clamp to a visible default;
  missing optional args default sensibly; learner mistakes produce *a picture*,
  not a traceback, wherever reasonable. (Genuine Python errors from the
  learner's own syntax still surface honestly — we hide our plumbing's errors,
  not theirs.)
- **`grid` is an iterator, not a callback.** Idiomatic Python and easier to
  teach:
  ```python
  for cell in grid(6, 6):
      fill(random_color())
      circle(cell.center_x, cell.center_y, 26)
  ```
  Each `cell` exposes `col, row, x, y, width, height, center_x, center_y`.
- **`animate` hides the loop entirely.** The learner writes a `draw(time)`
  function and hands it over; they never see `while`, events, or `flip()`:
  ```python
  def draw(time):
      background("#fdf6e3")
      circle(width / 2, height / 2, 20 + sin(time) * 12)

  animate(draw)
  ```
- **Coordinates:** `(0, 0)` top-left, `x` right, `y` down. State this once in
  `VOCABULARY.md`; never make the learner derive it.
- **Repeatable randomness.** `seed(n)` makes a sketch reproducible; same seed,
  same picture. The first task depends on this.

When adding any public function, also add: its type hints, a one-line
docstring a beginner can read, and a line in `VOCABULARY.md`. These three move
together — never one without the others.

---

## 8. Engineering standards & tooling

- **Python version:** **[Verify]** the current stable CPython and target it;
  pin a minimum that supports the substrate. State it in `pyproject.toml`.
- **Type checking:** run a static checker in CI on the *library* source (the
  public API must be correctly typed). Learner code is never type-checked by us.
  **[Verify]** the current recommended checker and its packaging before adding.
- **Tests:** unit tests for the non-visual logic (`grid` cell math, `random`
  ranges/reproducibility under a fixed `seed`, clamping behaviour). Visual
  output itself need not be pixel-tested at this stage; test the math behind it.
  Keep tests readable — they double as executable documentation of the API.
- **Formatting/linting:** adopt one formatter and one linter, configured in
  `pyproject.toml`, run in CI. **[Verify]** current tooling before pinning.
- **Packaging:** `pyproject.toml`, installable with a single `pip install`.
  The install step is the learner's cliff edge (§3) — keep dependencies minimal
  and the install command to one line.
- **No browser/web concepts.** No JS, no HTML, no CDN, no Pyodide. This is
  native Python. (Recorded because the sibling project was web-based.)

---

## 9. Phased plan

Build in order. Do not start a phase whose inputs are still **[Open]**. End each
phase with a short note to the owner: what's done, what you assumed, what needs a
decision.

**Phase 0 — Verify the ground (no feature code).**
Resolve §5.1 by verifying, from live sources, the current state of each
substrate candidate: existence, current version, install weight, whether `py5`
still needs Java, and immediate- vs retained-mode fit. Verify the §5.3 PyPI
name, the §8 Python version, and current checker/formatter/test tooling.
Deliver a one-page recommendation. **Stop and get the owner's substrate call.**

**Phase 1 — Core draw (read-only, no animation).**
Once the substrate is confirmed: `canvas` (window + surface), `shapes`,
`color`. A learner can draw a static composition with `from draw import *`.
Ship 2–3 example sketches. This is the riskiest integration; get it solid
before anything else.

**Phase 2 — Loops & randomness.**
`repeat`, `grid` (as an iterator, §7), the `rand` module with reproducible
`seed`. Add examples that produce grids of shapes and seeded variation.

**Phase 3 — Animation & input.**
`animate(draw)` hiding the loop; basic mouse/keyboard exposed as simple
readable values *if* the substrate makes it clean. Re-confirm scope with the
owner before adding input — it may belong later.

**Phase 4 — Curriculum.**
`VOCABULARY.md` (the complete flat list) and `TASKS.md` (numbered modify-this
tasks, each tagged with the concept it teaches — randomness, loops,
expressions, conditionals, animation). The task arc must go from "change one
number" to "write a draw function that reacts to time." This is core
deliverable value, not an afterthought.

**Phase 5 — Onboarding & distribution (the make-or-break phase).**
Resolve §5.4 with the owner, then implement the chosen path so the learner's
first run is frictionless: a single documented install/run command, a beginner
editor recommendation, and a "first sketch in under five minutes" guide. Test
the whole path on a clean machine as if you were a beginner. If a learner can't
get a circle on screen quickly, the project has failed regardless of how good
the library is.

**Later / [Open] — Platform layer.**
Only if §5.2 is defined by the owner. Do not pre-build for it.

---

## 10. Out of scope (do not build unless the owner asks)

- Any web/browser/Pyodide rendering, or shared code with the sibling project.
- The "platform" layer (lesson runner, accounts, progress, hosting) until §5.2
  is defined.
- Engineering abstractions with no learner payoff: plugin systems, async,
  message queues, deep class hierarchies, configuration frameworks.
- Pixel-level visual regression testing at this stage.
- Multi-language support. This is Python-only by decision (§4).

---

## 11. Definition of done for the seed stage

You have done your job for now when:

1. Phase 0 is delivered and the owner has made the §5.1 substrate call.
2. The §5 open decisions each have a written recommendation awaiting the owner.
3. Phase 1 is shippable on the confirmed substrate: a learner can
   `from firstpaint import *` and draw a static picture, with at least two
   runnable examples and tests for the non-visual logic.

Then stop and report. Do not run ahead into later phases or the platform layer
without the owner's go-ahead.
