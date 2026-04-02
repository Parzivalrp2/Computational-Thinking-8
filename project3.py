# Horse Racing
from utils import *

# Section 1 - Variables
x1 = 0
y1 = 200

x2 = 0
y2 = 100

x3 = 0
y3 = 0

x4 = 0
y4 = -100



# Section 2 - Setup
# # TODO - use your own background, and set your four turtles to images of your choice
set_background("grass")
t1 = create_sprite("horse1",x1,y1)
t2 = create_sprite("horse2",x2,y2)
t3 = create_sprite("horse3",x3,y3)
t4 = create_sprite("horse4",x4,y4)


# # Section 3 - Racing
i2 = 0
for i in range(100):
    if i == i2 + 10 or i == 0:
        speed1 = random.randint(5,15)
        speed2 = random.randint(5,15)
        speed3 = random.randint(5,15)
        speed4 = random.randint(5,15)
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
    time.sleep(0.1)


# # Section 4 - Winner
# # TODO - complete the elif for player 2 winning
# # TODO - write another elif for player 3 and player 4
# s5 = create_sprite("alien",-200,-200)
# if x1 >= x2 and x1 >= x3 and x1 >= x4:
#     s5.write("Player 1 wins!")
# elif
#     s5.write("player 2 wins!")


turtle.exitonclick()