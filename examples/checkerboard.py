"""A two-tone checkerboard, then a seeded shower of stars on top.

Demonstrates ``grid``, ``pick`` for choosing from a small palette, and
``random_int`` for variable sizes. With the seed fixed, the picture is
the same every time you run it.
"""

from firstpaint import *

canvas(600, 600)
background("#222")
no_stroke()

# checkerboard
for cell in grid(8, 8):
    if (cell.col + cell.row) % 2 == 0:
        fill("#f4e4bc")
    else:
        fill("#3d2c1e")
    rect(cell.x, cell.y, cell.width, cell.height)

# seeded sprinkle of dots
seed(123)
palette = ["#e63946", "#2a9d8f", "#f4a261", "#e9c46a"]
for _ in repeat(60):
    fill(pick(palette))
    circle(random_int(0, 600), random_int(0, 600), random_int(3, 10))

show()
