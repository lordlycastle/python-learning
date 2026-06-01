"""A small sun on warm paper.

The shortest sketch we can ship: one canvas, one background, one circle.
Change any number and run it again — watch where the sun moves.
"""

from firstpaint import *

canvas(600, 600)
background("#fdf6e3")

fill("#e67e22")
no_stroke()
circle(300, 220, 110)

show()
