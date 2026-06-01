"""A grid of confetti dots, one random colour each.

The §7 reference example. Demonstrates ``grid`` + ``random_color`` + a fixed
``seed`` for reproducibility. Change the seed → different picture. Change
the grid size → more or fewer dots. Same code shape either way.
"""

from firstpaint import *

canvas(600, 600)
background("#0f1117")
no_stroke()

seed(7)

for cell in grid(10, 10):
    fill(random_color())
    circle(cell.center_x, cell.center_y, 22)

show()
