def clear():
    print ('\033[1A' + '\033[K')
def inputf():
    input = input()
    if input == "exit":
        quit()
    else:
        return input

print("unnamed~> what is your name?")
username = inputf()
clear()
print(f"{username}(you)~> {username}")
username = (username + "(you)")
print("unnamed~> what is my name")
name = inputf()
clear()
print(f"{username}~> {name}")
print(f"{name}~> what country do you live in?")
country = inputf()
clear()
print(f"{username}~> {country}")
print(f"{name}~> cool! whats it like there?")
inputf()
clear()
print(f"{name}~> interesting!")
