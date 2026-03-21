import time
import sys
correct = 0
wrong = 0
lives = 5
questions = 0
def question(question,answers,timelimit, correct_ans):
    global correct
    global wrong
    global lives
    global questions
    questions += 1
    answers_str = ""
    for i in range(len(answers)):
        answers_str = answers_str + str(i+1) + ": " + str(answers[i]) + ", "
    
    timebf = time.time()
    ans = int(input(question + ":  " + answers_str + ":  "))
    timeaf = time.time()
    if timeaf-timebf > timelimit:
        wrong += 1
        lives -= 1
        print("lol you took too long")
    if ans in correct_ans:
        correct += 1
    else:
        wrong += 1
        lives -= 1
    if lives < 1 or correct == 0 and questions > 2:
        print("You Lost :(")
        sys.exit()
        
    print(f"Lives: {lives}")

question("who invented asymmetric encryption?", ["Whitfield Diffie","Martin Hellman","Clifford Cocks","William Jevons", "nobody"],10,[1,2,3])
question("Best?", ["Zed","VSCode","Vim","notepad++"],5,[1])
question("Worst?", ["Apple","Microsoft","Google","Trick Question, its all"],5,[4])
question("When did the russian revolution occur?", ["1940","1897","1963","1917","1920","1817"],10,[4])
question("Who is the current fastest runner on the 1k", ["Usain Bolt", "Noah Ngeny", "Sebastian Coe","Gladys Lunn"],10,[2])
question("1",[1,2],0,[1])
question("1",[1,2],0,[1])
question("1",[1,2],0,[1])
question("1",[1,2],0,[1])
question("1",[1,2],0,[1])
question("1",[1,2],0,[1])

print("You won :)")