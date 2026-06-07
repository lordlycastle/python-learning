# TASKS

A path of small changes. Each task starts with a sketch you can run. Then you change one or two things and see what happens. Don't skip ahead — every task adds one new idea on top of the last.

If anything stops working, undo your last change. Run it. You're back where you were.

---

## Task 1 — Make something appear

**Concept:** running a sketch.

Type this into a new file called `sketch.py` and run it.

```python
from firstpaint import *

canvas(600, 600)
background("#fdf6e3")

fill("#e67e22")
circle(300, 300, 100)

show()
```

You should see an orange circle on cream paper. If you don't — check that you saved the file, and that you wrote every line exactly as above.

---

## Task 2 — Change one number

**Concept:** the numbers are levers.

In Task 1's sketch, change the `100` in `circle(300, 300, 100)` to `250`. Run it again.

Now change it to `20`. Run it again.

The third number in `circle` is the radius. Bigger number, bigger circle.

---

## Task 3 — Move the circle

**Concept:** coordinates.

Take Task 1's sketch and try each of these in turn. Run after each.

- `circle(100, 300, 100)`
- `circle(500, 300, 100)`
- `circle(300, 100, 100)`
- `circle(300, 500, 100)`

The **first** number is `x` (how far right). The **second** number is `y` (how far down).

`(0, 0)` is the top-left of the canvas. `(600, 600)` is the bottom-right.

---

## Task 4 — Change the colour

**Concept:** colours by name and by code.

Replace `"#e67e22"` in your sketch with each of these in turn:

- `"red"`
- `"steelblue"`
- `"#7c3aed"`
- `(34, 197, 94)`

The first two are colour **names**. The third is a **hex code** (a colour written as a number in base 16). The fourth is **three numbers** — red, green, blue — each 0 to 255.

---

## Task 5 — Two shapes

**Concept:** shapes draw in order.

Change your sketch to this:

```python
from firstpaint import *

canvas(600, 600)
background("#fdf6e3")

fill("#e67e22")
circle(300, 300, 200)

fill("#1d3557")
circle(300, 300, 80)

show()
```

A small navy circle sits inside a big orange one.

Now **swap** the two `fill`/`circle` blocks — put the navy one first. Run it.

The navy circle disappears. It's still being drawn, but the orange circle is drawn **after** it, on top.

The rule: later lines draw on top of earlier lines.

---

## Task 6 — Outlines

**Concept:** stroke vs fill.

Try this sketch:

```python
from firstpaint import *

canvas(600, 600)
background("#fdf6e3")

stroke("#222")
fill("#fcd34d")
circle(300, 300, 150)

show()
```

You get a yellow circle with a thin black outline.

Now add `no_fill()` before `circle(...)`. The middle goes away — only the outline is left.

Take `no_fill()` out and add `no_stroke()` instead. The outline goes away — only the middle is left.

---

## Task 7 — More shape kinds

**Concept:** four shape functions.

Build this picture by typing the lines in:

```python
from firstpaint import *

canvas(600, 400)
background("#cce7ff")
stroke("#222")

fill("#f6c177")
rect(180, 180, 240, 180)

fill("#b94a3b")
triangle(160, 180, 300, 60, 440, 180)

fill("#5a3825")
square(280, 280, 80)

show()
```

A simple house. Then change one thing about it. Make the door taller. Make the roof come further down. Move the whole house left.

The shapes you used:

- `rect(x, y, width, height)` — `(x, y)` is the top-left corner
- `triangle(x1, y1, x2, y2, x3, y3)` — three corners
- `square(x, y, size)` — like rect but width = height

---

## Task 8 — Many shapes the easy way

**Concept:** loops with `repeat`.

Type this in:

```python
from firstpaint import *

canvas(600, 200)
background("#fdf6e3")
no_stroke()
fill("#2b9eb3")

for i in repeat(10):
    square(i * 60 + 5, 60, 50)

show()
```

Ten squares in a row.

The body of the `for` loop runs 10 times. Each time, `i` is a different number: 0, then 1, then 2, … up to 9. The first square is at `x = 0 * 60 + 5 = 5`. The next is at `65`. Then `125`. And so on.

Change the `10` to `20`. Change the canvas width to match. Change the spacing.

---

## Task 9 — A grid

**Concept:** stepping through 2D.

```python
from firstpaint import *

canvas(600, 600)
background("#0f1117")
no_stroke()
fill("#f4e4bc")

for cell in grid(6, 6):
    circle(cell.center_x, cell.center_y, 30)

show()
```

36 cream circles arranged in a 6×6 grid.

`grid(6, 6)` divides the canvas into 6 columns and 6 rows — 36 cells. The loop visits each one in order. `cell.center_x` and `cell.center_y` are the middle of that cell.

Change `grid(6, 6)` to `grid(10, 10)`. Change it to `grid(2, 12)`.

---

## Task 10 — Random colours

**Concept:** randomness.

Change the body of your grid loop so it picks a new colour each time:

```python
for cell in grid(6, 6):
    fill(random_color())
    circle(cell.center_x, cell.center_y, 30)
```

Run it. A grid of random colours.

Run it **again**. Different colours.

---

## Task 11 — Same picture every time

**Concept:** seeding.

Add one line above the loop:

```python
seed(7)
for cell in grid(6, 6):
    fill(random_color())
    circle(cell.center_x, cell.center_y, 30)
```

Now run it twice. **Same picture both times.**

Change `7` to `8`. Different picture, still repeatable.

The `seed` locks the random numbers to a starting point. Same seed → same sequence of "random" numbers → same picture.

---

## Task 12 — A choice for each cell

**Concept:** `if` inside a loop.

```python
from firstpaint import *

canvas(600, 600)
background("#222")
no_stroke()

for cell in grid(8, 8):
    if (cell.col + cell.row) % 2 == 0:
        fill("#f4e4bc")
    else:
        fill("#3d2c1e")
    rect(cell.x, cell.y, cell.width, cell.height)

show()
```

A checkerboard.

The `if` checks each cell: if the column plus the row is even, paint it cream. Otherwise, paint it brown.

Try changing the two colours. Try changing the condition to `cell.col % 3 == 0` and see what pattern you get.

---

## Task 13 — A sprinkle on top

**Concept:** combining what you know.

Below the checkerboard loop (but above `show()`), add:

```python
seed(123)
palette = ["#e63946", "#2a9d8f", "#f4a261", "#e9c46a"]
for _ in repeat(80):
    fill(pick(palette))
    circle(random_int(0, 600), random_int(0, 600), random_int(3, 10))
```

80 dots in random places, each one a random colour from your palette, each one a random size.

You're using **everything from this page** in one sketch.

---

## Task 14 — Your turn

**Concept:** an open task.

Make a sketch of your own. Pick something simple: a flag, a flower, a building, a face. Use whatever vocabulary you've learned. Don't worry about it being good.

When you can build a simple picture without looking at this page, you're ready for the next thing — making your picture move.

---

## Task 15 — A breathing circle

**Concept:** animation.

```python
from firstpaint import *

canvas(600, 600)

def draw(time):
    background("#fdf6e3")
    fill("#e67e22")
    no_stroke()
    circle(width / 2, height / 2, 60 + sin(time) * 30)

animate(draw)
```

A circle that grows and shrinks forever.

What changed:

- You wrote a function called `draw(time)`. firstpaint will call it 60 times a second.
- Each call, `time` is the number of seconds the sketch has been running.
- `sin(time)` is a number that smoothly wobbles between -1 and +1. Multiplied by 30, it gives a number between -30 and +30. Added to 60, that's a radius between 30 and 90.
- You called `animate(draw)` instead of `show()`. `animate` is its own loop. Don't put `show()` after it — `animate` already keeps the window open.

Close the window to stop the sketch.

---

## Task 16 — Faster, slower

**Concept:** scaling time.

In Task 15, change `sin(time)` to `sin(time * 4)`. Run it. The circle breathes four times faster.

Now try `sin(time * 0.3)`. Slower.

The number you multiply `time` by is the **speed** of the wobble.

Now change the `* 30` (the size of the wobble) to `* 100`. The circle grows and shrinks much more dramatically.

You now have two knobs: **how fast** (`time * 4`) and **how big** (`* 100`).

---

## Task 17 — A circle that orbits

**Concept:** `sin` and `cos` together.

```python
from firstpaint import *

canvas(600, 600)

def draw(time):
    background("#0f1117")
    fill("#fcd34d")
    no_stroke()
    x = width / 2 + cos(time) * 220
    y = height / 2 + sin(time) * 220
    circle(x, y, 22)

animate(draw)
```

A dot orbiting the centre.

`cos(time)` and `sin(time)` taken together trace a circle. Multiply both by the **radius** of the orbit. Add the **centre** of the orbit. That's it.

Try changing `220` to `100`. Smaller orbit. Try `300`. Bigger.

Try changing `time` to `time * 2`. Faster orbit.

---

## Task 18 — A wave of circles

**Concept:** animation inside a loop.

```python
from firstpaint import *

canvas(600, 300)

def draw(time):
    background("#fdf6e3")
    fill("#2b9eb3")
    no_stroke()
    for i in repeat(12):
        x = i * 50 + 25
        y = height / 2 + sin(time * 2 + i * 0.4) * 60
        circle(x, y, 18)

animate(draw)

```

Twelve circles, bobbing up and down out of sync.

The key trick: each circle's wobble is offset by `i * 0.4`. That's why the wave **travels** across the row instead of all dots moving in lockstep.

Change `0.4` to `0` and run it. Now they move together. Change it to `1.5` and run it. Now they're scattered.

---

## Task 19 — Your moving sketch

**Concept:** open task.

Pick one of your earlier sketches and make something in it move. The simplest move is "wobble one number with `sin(time)`." The next-simplest is "let `time` drive `x` or `y`."

You don't need to make the whole sketch animated. One moving thing is enough.

When you can do this, you've reached the end of the path that this page lays out. The library has more inside it, but everything you need to build something interesting is on this page.
