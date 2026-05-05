from utils import *

money = 0
employees = 1
factories = 1
factory_price = 1
factory_x = -300
employee_price = 1
income_percent_timer = 0
last_update = 0
income_time = 1
set_background("grass2")

# OPTIONAL: use this invisible alien to say a message
m1 = create_sprite("alien", -200,200)
m1.hideturtle()



# Section 2 - controls
# TODO - define an action. ex: def my_control()

# TODO - choose a key to do the action. ex: window.onkeypress(my_control, "space")

# TODO - make a second control
#increases employee by one for the price, and increases price
def hire_employee():
    global money
    global employees
    global employee_price
    if money >= employee_price:
        money -= employee_price
        employees += 1
        employee_price += round(employee_price/4, 2)

window.onkeypress(hire_employee, "n")

#Adds factory to screen and adds one to factories for price and adds to price
def buy_factory():
    global money
    global factories
    global factory_price
    global factory_x
    if money >= factory_price:
        money -= factory_price
        factories += 1
        factory_price += round(factory_price/4, 2)
        factory_x += 100
        y = -100
        create_sprite("factory",factory_x,y)
window.onkeypress(buy_factory, "e")

# The goal of this game is to make as much money as possible
# Section 3 - game loop
window.listen()
while True:
    income_percent_string = "<"
    #renders progress bar
    for i in range(round(income_percent_timer) // 5 - 1):
        income_percent_string += "-"
    #Adds pacman guy
    if (round(income_percent_timer) // 5) % 2 == 0:
        income_percent_string += "C"
    else:
        income_percent_string += "c"
    for i in range(20-round(income_percent_timer) // 5):
        income_percent_string += "#"
    income_percent_string += ">"
    m1.clear()
    m1.write(f"Money: ${round(money, 2)} \n Factory Price: ${round(factory_price, 2)} \n Employees: {employees} \n Employee Price: ${round(employee_price, 2)} \n Income: {income_percent_string}", font=("Courier New", 16, "normal"))
    if time.time() >= last_update + income_time - employees / 5:
        income_percent_timer += 5
        if income_percent_timer >= 100:
            income_percent_timer = 0
            money += factories
        last_update = time.time()
    time.sleep(0.01)
    window.update()
