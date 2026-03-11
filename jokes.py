import time
while True:
    response = input("Does Microsoft understand consent?   [Y]es/[R]emind Me in 3 Days: ")
    if response == "Y" or response == "y":
        response2 = input("What are the last 4 digits of your SSN: ")
        for i in response2:
            if i != "1" and i != "2" and i != "3" and i != "4" and i != "5" and i != "6" and i != "7" and i != "8" and i != "9" and i != "0":
                ssn = False
                break
            else:
                if len(response2) == 4:
                    ssn = True
                else:
                    ssn = False
        if ssn:
            print("Good Job!")
            
        else:
            print(f"{response2} is not a valid response")
        break
    elif response == "R" or response == "r":
        time.sleep(1)
    else:
        print(f"{response} is not a valid response")
        time.sleep(1)