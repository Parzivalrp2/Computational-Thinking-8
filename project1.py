def clear():
    print ('\033[1A' + '\033[K')

print("unnamed~> what is your name?")
username = input()
clear()
print(f"{username}~> {username}")
print("unnamed~> what is my name")
name = input()
clear()
print(f"{username}~> {name}")
print(f"{name}~> what country do you live in?")
country = input()
clear()
print(f"{username}~> {country}")

