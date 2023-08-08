import random
from tkinter import *
from visualization.ball import Ball
from constants.colors import COLORS
import time

window = Tk(className="Visualization")

WIDTH = 960
HEIGHT = 540
canvas = Canvas(window, width=WIDTH, height=HEIGHT)
canvas.pack()

balls = []
for i in range(random.randint(50, 250)):
    diameter = random.randint(0, 100)
    x = random.randint(25, WIDTH-diameter-25)
    y = random.randint(25, HEIGHT-diameter-25)
    balls.append(
        Ball(
            canvas,
            x,
            y,
            diameter,
            random.randint(-10, 10),
            random.randint(-10, 10),
            COLORS[random.randint(0, len(COLORS) - 1)]
        )
    )

while True:
    for ball in balls:
        ball.move()
    window.update()
    time.sleep(0.05)
