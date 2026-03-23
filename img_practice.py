# Section 1 - Your code
from utils import *
set_background("winter")

arrow = create_sprite("arrow.gif", 100, 100)


while True:
    time.sleep(0.25)
    arrow.right(25)
    arrow.tilt(90)
    window.update()