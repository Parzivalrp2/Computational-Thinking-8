import wordle_backend
import random
word = random.choice(wordle_backend.possible_answers)
for i in range(6):
    output = ""
    guess = input()
    if guess not in wordle_backend.allowed_guesses:
        print(f"Invalid Guess")
        break
    for x in range(len(guess)):
        if guess[x] == word[x]:
            output += "🟩"
        elif guess[x] in word:
            output += "🟨"
        else:
            output += "🔲"
    print(output)
    if output == "🟩🟩🟩🟩🟩":
        print(f"You won in {i+1} guesses!")
        break
if output != "🟩🟩🟩🟩🟩": 
    print("you lost...")
        

