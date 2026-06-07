"""A row of circles bobbing up and down out of sync.

Each circle gets a different time offset (the ``i * 0.4``), so the wave
ripples across instead of moving every dot at the same instant.
"""

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
