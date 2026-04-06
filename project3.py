# Horse Racing
from utils import *

# Section 1 - Variables
x1 = 200
y1 = 200

x2 = 200
y2 = 100

x3 = 200
y3 = 0

x4 = 200
y4 = -100



set_background("grass")
t1 = create_sprite("horse1",x1,y1)
t2 = create_sprite("horse2",x2,y2)
t3 = create_sprite("horse3",x3,y3)
t4 = create_sprite("horse4",x4,y4)

one_finished = False
two_finished = False
three_finished = False
four_finished = False


i2 = 0
start_time = time.time()

for i in range(100):
    if i == i2 + 10 or i == 0:
        speed1 = -random.randint(10,50)
        speed2 = -random.randint(10,50)
        speed3 = -random.randint(10,50)
        speed4 = -random.randint(10,50)
        i2 = i
    x1 += speed1
    x2 += speed2
    x3 += speed3
    x4 += speed4

    t1.goto(x1, y1)
    t2.goto(x2, y2)
    t3.goto(x3, y3)
    t4.goto(x4, y4)
    window.update()
    if x1 < -300:
        winner = 1
        break
    elif x2 < -300:
        winner = 2
        break
    elif x3 < -300:
        winner = 3
        break
    elif x4 < -300:
        winner = 4
        break
    time.sleep(0.1)



s5 = create_sprite(None,-200,-200)

print(winner)
s5.write(f"Horse {winner} is the winner!",font=("ariel",24,"normal"))


turtle.exitonclick()