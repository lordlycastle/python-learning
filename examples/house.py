"""A flat-colour house, three shapes deep.

Demonstrates the three core shapes (rect, triangle, square) and a stroke
that's actually visible. Try changing the door's height.
"""

from firstpaint import *

canvas(600, 600)
background("#cce7ff")

stroke("#222")

# walls
fill("#f6c177")
rect(180, 280, 240, 220)

# roof
fill("#b94a3b")
triangle(160, 280, 300, 140, 440, 280)

# door
fill("#5a3825")
square(280, 380, 80)

# window
fill("#ffffff")
square(210, 320, 50)

show()
