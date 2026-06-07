# VOCABULARY

Everything you can write in a firstpaint sketch. One word, one job.

At the top of every sketch, write this line once:

```python
from firstpaint import *
```

Now every name on this page works.

---

## How positions work

- `(0, 0)` is the **top-left** corner of the canvas.
- `x` grows to the **right**.
- `y` grows **downward**.
- Sizes are in pixels.

So `circle(300, 200, 50)` puts a circle 300 across and 200 down, with radius 50.

---

## How colours work

Anywhere a colour is asked for, you can write it in any of these ways:

- A hex code: `"#fdf6e3"`, `"#f80"` (three letters is fine — it expands)
- A name: `"red"`, `"steelblue"`, `"hotpink"`
- Three numbers — red, green, blue — each 0 to 255: `(255, 100, 50)`
- Four numbers if you also want transparency: `(255, 100, 50, 128)`
- A single grey value 0 to 255: `128`

If you write a colour that doesn't make sense, the picture will turn bright pink so you can find the mistake.

---

## The canvas

### `canvas(width, height, title)`

Open the canvas. Call this once near the top of your sketch.

```python
canvas(600, 400, "my sketch")
```

If you don't call it, you get a 600×600 canvas by default.

### `background(color)`

Paint the whole canvas one colour. Wipes anything drawn before it.

```python
background("#fdf6e3")
```

### `show()`

Keep the window open until you close it. Put this at the bottom of your sketch.

```python
show()
```

### `width` and `height`

The size of your canvas, as numbers you can use in maths.

```python
circle(width / 2, height / 2, 50)
```

---

## Colours

### `fill(color)`

Sets the colour used for the **inside** of shapes drawn after this line.

```python
fill("orange")
circle(300, 300, 60)
```

### `no_fill()`

Stop filling shapes in. They will only have an outline (if `stroke` is set).

### `stroke(color)`

Sets the colour used for the **outline** of shapes drawn after this line.

```python
stroke("#222")
```

### `no_stroke()`

Stop drawing outlines. Shapes drawn after this line have no edge.

---

## Shapes

### `circle(x, y, radius)`

A circle. `(x, y)` is its **centre**.

```python
circle(300, 300, 80)
```

### `rect(x, y, width, height)`

A rectangle. `(x, y)` is its **top-left corner**.

```python
rect(100, 50, 200, 150)
```

### `square(x, y, size)`

A square. Same as `rect(x, y, size, size)`.

```python
square(50, 50, 80)
```

### `line(x1, y1, x2, y2)`

A straight line from one point to another. Uses the current `stroke` colour.

```python
line(0, 0, 600, 600)
```

### `triangle(x1, y1, x2, y2, x3, y3)`

A triangle made from three corner points.

```python
triangle(100, 400, 300, 100, 500, 400)
```

### `text(message, x, y, size)`

A piece of text. `(x, y)` is its top-left corner. `size` is the height in pixels (defaults to 20). Uses the current `fill` colour.

```python
text("hello", 100, 100, 32)
```

---

## Loops

### `repeat(n)`

Run a block of code `n` times. Use it with a `for` loop.

```python
for i in repeat(10):
    circle(i * 60 + 30, 300, 20)
```

The variable `i` counts: 0, 1, 2, … up to but not including `n`.

If you don't need the counter, use `_` instead:

```python
for _ in repeat(50):
    circle(random_int(0, 600), random_int(0, 600), 10)
```

### `grid(cols, rows)`

Split the canvas into a grid and step through every cell, one by one.

```python
for cell in grid(6, 6):
    fill(random_color())
    circle(cell.center_x, cell.center_y, 26)
```

Each `cell` knows:

- `cell.col`, `cell.row` — which column and row it is (starting at 0)
- `cell.x`, `cell.y` — the top-left corner of the cell in pixels
- `cell.width`, `cell.height` — how big the cell is in pixels
- `cell.center_x`, `cell.center_y` — the middle of the cell in pixels

---

## Randomness

### `seed(n)`

Lock the random numbers to a number you choose. Same seed → same picture, every time.

```python
seed(42)
```

Change the seed and the picture changes. Run again with the same seed and you get the same picture back.

### `random_int(low, high)`

A random whole number between `low` and `high` — both included.

```python
random_int(1, 6)   # like rolling a die
```

### `random_number(low, high)`

A random decimal number between `low` and `high`. With no arguments, you get a number between 0 and 1.

```python
random_number()           # 0.0 to 1.0
random_number(0.5, 1.5)   # 0.5 to 1.5
```

### `pick(items)`

Pick one item at random from a list.

```python
pick(["red", "blue", "yellow"])
```

If the list is empty, you get `None`.

### `random_color()`

A random colour that's bright enough to see. Different every time — unless you've set a `seed`.

```python
fill(random_color())
```

---

## Animation

### `animate(draw)`

Hand the library a function called `draw` and watch your sketch come alive. firstpaint will call your `draw` function 60 times a second. Each time, it hands you the number of seconds the sketch has been running.

```python
def draw(time):
    background("#fdf6e3")
    circle(width / 2, height / 2, 20 + sin(time) * 12)

animate(draw)
```

Use `animate(draw)` **instead of** `show()`, not as well as. `animate` runs its own loop until you close the window.

### `sin(x)`

A number that smoothly wobbles between -1 and +1 as `x` grows. Useful for "make this thing breathe" or "make this thing wave."

```python
sin(0)        # 0
sin(pi / 2)   # 1
sin(pi)       # 0 (back to zero — one full sweep takes 2 * pi)
```

If you multiply, you stretch the wobble: `sin(time) * 50` wobbles between -50 and +50.

### `cos(x)`

Like `sin`, but starts at 1 instead of 0. Pair `cos` and `sin` together to trace a circle:

```python
x = width / 2 + cos(time) * 200
y = height / 2 + sin(time) * 200
circle(x, y, 20)
```

### `pi`

The number 3.14159... You'll see it whenever you're thinking about full turns. `sin` and `cos` finish a full wobble every `2 * pi`.
