"""A dot orbiting the centre.

``cos(time)`` and ``sin(time)`` taken together trace a circle — that's
their whole job. Multiply both by 220 to set the orbit's radius.
"""

from firstpaint import *

canvas(600, 600)


def draw(time):
    background("#0f1117")
    no_stroke()

    # the orbit path, faintly
    fill("#1f2531")
    circle(width / 2, height / 2, 220)

    # the orbiting dot
    fill("#fcd34d")
    x = width / 2 + cos(time) * 220
    y = height / 2 + sin(time) * 220
    circle(x, y, 22)


animate(draw)
