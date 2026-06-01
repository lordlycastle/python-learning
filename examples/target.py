"""A target — concentric circles, ending with a tiny label.

Demonstrates that drawing later puts shapes *on top*. Try reordering the
circles and watch what disappears.
"""

from firstpaint import *

canvas(600, 600)
background("#0f1117")
no_stroke()

fill("#e63946")
circle(300, 300, 220)

fill("#f1faee")
circle(300, 300, 170)

fill("#e63946")
circle(300, 300, 120)

fill("#f1faee")
circle(300, 300, 70)

fill("#e63946")
circle(300, 300, 25)

fill("#f1faee")
text("bullseye", 250, 470, 28)

show()
