import random

num_of_letters = int(input("How many letters?  "))
num_of_lines = 0
wordbank = []
with open (f"E:\Coding\wordle\{num_of_letters}letter.txt") as f:
    for line in f:
        num_of_lines += 1
        wordbank.append(line.strip('\n'))

    rand_num = random.randint(1, num_of_lines+1)

answer = wordbank[rand_num]
print(answer)
print("Your word has been selected!")

def check_word_validity(wordbank, check_word):
    for counter, line in enumerate(wordbank):
        if check_word == line:
            return True
        elif counter + 1 == num_of_lines:
            return False
        
gaps = ["_"]*num_of_letters
print(gaps)

for num in range(0,num_of_letters):
    guess = (input("Your guess?  "))
    if guess == answer:
        print("Correct!")
        break
    elif len(guess) == num_of_letters and check_word_validity(wordbank, guess):
        for char in guess:
            if char in answer:
                print(f"There is a \"{char}\" in answer")
    
    else:
        print("Invalid Guess!")

