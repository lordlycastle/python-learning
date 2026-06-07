"""A single circle, breathing.

The §7 reference example. ``sin(time)`` wobbles between -1 and +1 about
once every 6.28 seconds; multiplying by 30 stretches that into a 60-pixel
swing on the radius.
"""

from firstpaint import *

canvas(600, 600)


def draw(time):
    background("#fdf6e3")
    fill("#e67e22")
    no_stroke()
    circle(width / 2, height / 2, 60 + sin(time) * 30)


animate(draw)
