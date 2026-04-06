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



# Section 2 - Setup
# # TODO - use your own background, and set your four turtles to images of your choice
set_background("grass")
t1 = create_sprite("horse1",x1,y1)
t2 = create_sprite("horse2",x2,y2)
t3 = create_sprite("horse3",x3,y3)
t4 = create_sprite("horse4",x4,y4)

one_finished = False
two_finished = False
three_finished = False
four_finished = False

# # Section 3 - Racing
i2 = 0
start_time = time.time_ns()
for i in range(100):
    if i == i2 + 10 or i == 0:
        speed1 = -random.randint(5,15)
        speed2 = -random.randint(5,15)
        speed3 = -random.randint(5,15)
        speed4 = -random.randint(5,15)
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
    if x1 <= -400:
        one_finished = True
        one_time = time.time_ns()
    if x2 <= -400:
        two_finished = True
        two_time = time.time_ns()
    if x3 <= -400:
        three_finished = True
        three_time = time.time_ns()
    if x4 <= -400:
        four_finished = True
        four_time = time.time_ns()
    if one_finished and two_finished and three_finished and four_finished:
        break
    time.sleep(0.1)

print(x1,x2,x3,x4)

# # Section 4 - Winner
# # TODO - complete the elif for player 2 winning
# # TODO - write another elif for player 3 and player 4
# s5 = create_sprite("alien",-200,-200)
# if x1 >= x2 and x1 >= x3 and x1 >= x4:
#     s5.write("Player 1 wins!")
# elif
#     s5.write("player 2 wins!")


turtle.exitonclick()