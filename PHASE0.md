# Phase 0 — Verification report (v2)

> Per CLAUDE.md §9. No feature code yet. Every claim tagged per §1 legend.
> Verified 2026-05-31, revised 2026-05-31 after owner feedback.
> Target OS: Windows + macOS.

---

## Owner decisions captured so far

- **§5.1 Substrate — pygame-ce.** **[Locked]** (owner confirmed; "pygame's recent PRs are mostly spam"). Same conclusion the verification reached independently — see §A.
- **§5.4 Onboarding — PyCharm (Community / "Core" tier).** **[Locked]** (owner override for industry-standard exposure). Important friction note in §C below — read it.
- **§5.2 Scope — explicitly deferred** until the core library + curriculum prove the methodology. **[Deferred]**
- **§5.3 Name — `firstpaint`.** **[Locked]** 2026-05-31. PyPI hard-verified available on this date (project page, simple index, and `first-paint` / `first_paint` PEP 503 equivalents all returned no project). Distribution and import name are the same: `pip install firstpaint` → `from firstpaint import *`. See §B for the path that got us here.

---

## A. §5.1 Substrate — pygame-ce locked ✅

Owner confirmed; verification stands.

- **pygame-ce 2.5.7**, released **2 March 2026**. [Verified]
- Active fork by former core pygame devs; upstream pygame has stalled. [Verified]
- Supports **Python 3.10 – 3.14**; dropped 3.9 in 2.5.7. pygame-ce 2.5.6 was the first with Python 3.14 wheels — upstream pygame lagged 3.14 entirely. [Verified]
- macOS: **universal2** wheels (one wheel covers Intel + Apple Silicon). [Verified]
- Windows: prebuilt wheels. [Verified]
- Install: `pip install pygame-ce --upgrade` — single command, SDL bundled in the wheel. [Verified]

Alternatives ruled out per v1 of this report (py5 needs JDK; turtle is retained-mode; Jupyter adds non-standard execution model).

---

## B. §5.3 Name — pivot to compound names

### What the verification surfaced

Single-word evocative names on PyPI are almost all taken. Even when the squatter is dead, the slot blocks us. Verified [Verified] taken: `draw`, `sketch`, `sketchpy`, `pyplay`, `pixie`, `visualpython` (and by PEP 503 normalization `visual-python`), `glyph`, `motif`, `bloom` (active!), `forma`, `mote`, `tessera`, `vellum`, `kineo`, `numen`. PyPI also returned anti-bot challenges for `lumen`, `prism`, `plinth` — I treat those as "very likely taken" since both `lumen` (Holoviz) and `prism` are known Python packages [Inference], not [Verified].

### Recommendation: go compound, not single-word

The whole modern ecosystem does this — `numpy`, `matplotlib`, `scikit-learn`, `streamlit`, `manim`, `pygame-ce`. Compound names also self-explain on a first read and survive search.

Each candidate below would still need a real PyPI registration attempt before adoption — absence-of-page on PyPI is suggestive, not conclusive.

**Directions, with sample names per direction.** Pick a direction first; I'll do a real availability sweep on a shortlist after.

| Direction | What it signals | Sample names |
|---|---|---|
| **Compound around "first / start / hello"** | The learner's first thing. Honest about the audience. | `firstpaint`, `firstline`, `helloart`, `helloshape` |
| **Compound around "play / sandbox / studio"** | Playful, suggests modify-and-see. | `pyplayground`, `codestudio`, `sketchstudio`, `paintbox` |
| **Compound around "loop / frame / canvas"** | Names what the library actually owns (the loop, the canvas). | `easycanvas`, `frameloop`, `canvaskit` |
| **Made-up / portmanteau** | No baggage; memorable; harder to collide. | `paintly`, `drawio` (likely taken — drawio is a thing — skip), `paintling`, `crayonpy`, `glyphic` |
| **Compound around "studio" + audience** | Curriculum-friendly. | `learnpaint`, `studypaint`, `classpaint` |

My picks if I had to choose three to verify hard: **`firstpaint`**, **`paintbox`**, **`easycanvas`**. They each pass §7's "read aloud and picture what appears" test for the project name itself, and they signal "for beginners" without saying "for beginners."

**Note on `draw` as the import.** Even if the project name is `firstpaint`, the `from draw import *` import is still blocked (the 2015 `draw` package exists). Either:
- Use a different import name aligned with the project — e.g. `from firstpaint import *`. [Recommended — keeps PyPI and import consistent, learner sees one word.]
- Pursue PEP 541 transfer for `draw` (slow, uncertain — the maintainer was last active in 2015).

I recommend keeping the project name and import name **the same**, e.g. `pip install firstpaint` → `from firstpaint import *`. One word for the learner to remember.

### What I need from the owner

Pick a **direction** (one of the rows above, or describe a new one). Then I'll do a focused PyPI availability sweep on 5–8 candidates in that direction and bring back a short list.

---

## C. §5.4 Onboarding — PyCharm, with an honest tradeoff

Owner override: **PyCharm Community ("Core" tier) as the official IDE** — industry-standard exposure for students.

### What I verified

- "PyCharm Community Edition" no longer exists as a separate product. **Starting PyCharm 2025.1**, JetBrains unified Community + Professional into a single PyCharm download. The free tier is now called **"PyCharm Core"** with the same open-source feature set as old CE; every install starts with a 30-day Pro trial that downgrades to Core after. **[Verified]**
- Current version: **PyCharm 2026.1.2**. [Verified]
- Windows + macOS installers available; macOS has Intel and Apple Silicon builds. [Verified]
- **Packages tool window:** real and free in the Core tier. Search + install with no terminal. [Inference — long-standing PyCharm CE feature; not specifically re-verified this session but well documented.]

### Friction note — please read

Per JetBrains' own current docs (`jetbrains.com/help/pycharm/configuring-python-interpreter.html`): **"you need to ensure that you've downloaded Python and installed it in your system."** The free Core tier does **not** install Python for you — it configures interpreters against a Python that is already installed.

[Inference, not [Verified]] PyCharm Pro's "Add Interpreter → Download Python" feature exists in 2024+ builds, and may or may not be available in the Core tier — the docs I found do not confirm it for Core. Worth a hands-on check on a clean machine in Phase 5.

**Practical onboarding flow for the learner (Windows + macOS), as I currently understand it:**

1. Download and install **Python 3.14** from `python.org`. (Step the learner must do separately.)
2. Download and install **PyCharm** from `jetbrains.com/pycharm/download`. (One installer; Java is bundled — no JDK install.)
3. First launch: create a new project; PyCharm asks which Python — point it at the one from step 1. Or accept PyCharm's offered virtualenv default.
4. **Packages tool window → search `pygame-ce` → Install.**
5. Open `examples/first.py` → green Run button → circle appears.

That's two installers instead of one. It's the honest tradeoff for the "industry-standard IDE" win. **Phase 5 verification should test the whole path on a clean Windows and macOS machine** with literal click-by-click screenshots — if step 1 trips a learner with a `PATH` error or an x64-vs-arm64 confusion, we should know that before students do.

### What I'm not recommending

- **Thonny** is a better pure-onboarding fit (bundles Python, zero separate install) — flagging it here only so the tradeoff is visible. Owner has chosen industry-standard exposure over zero-friction, which is a defensible call.
- **Mu editor** is sunset (Dec 2024 announcement, retired in 2025) — do not recommend.

---

## D. §8 Engineering tooling — verified picks (unchanged)

| Concern | Choice | Confidence |
|---|---|---|
| Python target | **Min 3.11**, develop on **3.14** | [Verified] 3.14.5 is current stable; 3.13.13 is current 3.13 maintenance; pygame-ce 2.5.7 covers 3.10–3.14. |
| Linter + formatter | **Ruff** | [Verified] |
| Type checker | **Pyright** | [Verified] 98% typing-spec conformance; native VS Code/PyCharm integration. |
| Test runner | **pytest** | [Verified] |
| Dev package manager | **uv** (Astral) | [Verified] Used by us, not learners. Learners type `pip install` inside PyCharm's Packages tool. |

---

## E. §5.2 Scope — deferred ✅

Owner: "first working product is focused on testing this methodology to teach and student accessibility." Platform layer parked until the core library + curriculum prove the methodology. **Do not design or build for it.**

---

## Phase 0 closed — Phase 1 unblocked

Everything is locked or deferred:

- ✅ Substrate: pygame-ce
- ✅ Python target: 3.11+, dev on 3.14
- ✅ Tooling: Ruff, Pyright, pytest, uv
- ✅ IDE: PyCharm Core
- ✅ §5.3 name: **`firstpaint`** ([Verified] available 2026-05-31; re-check on real registration)
- ✅ §5.2 scope: deferred until methodology proves out

Phase 1 starts on the owner's say-so: `src/firstpaint/` + `canvas`, `shapes`,
`color` against pygame-ce, plus 2–3 example sketches and tests for the non-visual
logic, per CLAUDE.md §9.

---

## Sources

- pygame-ce: [PyPI](https://pypi.org/project/pygame-ce/), [GitHub releases](https://github.com/pygame-community/pygame-ce/releases)
- PyCharm unified product: [JetBrains: PyCharm, the Only Python IDE You Need (Apr 2025)](https://blog.jetbrains.com/pycharm/2025/04/unified-pycharm/), [What's New in PyCharm 2026.1](https://blog.jetbrains.com/pycharm/2026/03/what-s-new-in-pycharm-2026-1/), [Configure a Python interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html), [Quick start guide](https://www.jetbrains.com/help/pycharm/quick-start-guide.html), [Unified PyCharm overview](https://www.jetbrains.com/help/pycharm/unified-pycharm.html)
- Python releases: [3.14.0](https://www.python.org/downloads/release/python-3140/), [3.13.13](https://www.python.org/downloads/release/python-31313/), [endoflife.date](https://endoflife.date/python)
- Ruff: [docs.astral.sh/ruff](https://docs.astral.sh/ruff/)
- Pyright comparison: [pydevtools](https://pydevtools.com/handbook/explanation/how-do-mypy-pyright-and-ty-compare/)
- uv: [docs.astral.sh/uv](https://docs.astral.sh/uv/)
- Mu sunset: [Adafruit blog](https://blog.adafruit.com/2024/12/10/the-mu-python-code-editor-is-sunsetting-in-2025/)
- PyPI name checks: [draw](https://pypi.org/project/draw/), [visualpython](https://pypi.org/project/visualpython/), [sketch](https://pypi.org/project/sketch/), [sketchpy](https://pypi.org/project/sketchpy/), [glyph](https://pypi.org/project/glyph/), [motif](https://pypi.org/project/motif/), [bloom](https://pypi.org/project/bloom/), [forma](https://pypi.org/project/forma/), [mote](https://pypi.org/project/mote/), [tessera](https://pypi.org/project/tessera/), [vellum](https://pypi.org/project/vellum/), [kineo](https://pypi.org/project/kineo/), [numen](https://pypi.org/project/numen/)
