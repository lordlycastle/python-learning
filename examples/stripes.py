"""A row of squares using ``repeat``.

The simplest possible loop sketch. Each square is the same except for its
x position, which depends on the loop counter. Try changing the ``10`` and
watch the row get longer or shorter.
"""

from firstpaint import *

canvas(600, 200)
background("#fdf6e3")
no_stroke()

fill("#2b9eb3")
for i in repeat(10):
    square(i * 60 + 5, 60, 50)

show()
