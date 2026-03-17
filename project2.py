import time
import threading
points = 0
wrong = 0

def question(question,answers,timelimit, correct_ans):
    global points
    global wrong
    answers_str = ""
    correct_int = []
    for i in range(len(answers)-1):
        for x in correct_ans:
            if answers[i] == x:
                correct_int.append(i+1)
        answers_str = answers_str + str(i+1) + ": " + str(answers[i]) + ", "
    
    timebf = time.time()
    ans = int(input(question + ":  " + answers_str + ":  "))
    timeaf = time.time()
    if timeaf-timebf > timelimit:
        wrong += 1
    for i in correct_int:
        print(i)
        if ans == i:
            points += 1
            return
    wrong += 1

q1 = question("what is 1", [1,2,3,4],30,[1])

print(f"Points: {points}, Wrong: {wrong}")