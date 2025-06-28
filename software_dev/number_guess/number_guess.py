import random

print("\n")
print("Welcome to the Number Guessing Game!\n")
print("You'll be asked for guess a number between 1 and 10.")
print("If you guess the number correctly, you win.")
print("You have 3 attempts to guess the number. Ready? Let's go!!\n")

def show_score(past_attempts):
    if not past_attempts:
        print("No best score right now. Play a few games first!\n")
    else:
        print(f"The current best score is {min(past_attempts)} attempt(s)")

def start_game():
    num_to_guess = random.randint(1, 10)
    guesses = 0
    past_attempts = []
    play = input("Want to play the Number Guessing Game? (yes/no)\n").lower()
    if play != "yes":
            print("Okay sure. Thank you for playing!")
            exit()
    else:
        show_score(past_attempts)
    # Game loop
    while play == "yes":
        try:
            user_guess = int(input("Guess a number between 1 and 10:\n"))
            
            if user_guess < 1 or user_guess > 10:
                raise ValueError("Please guess a number within the given range\n")
            # Increment guesses
            guesses += 1
            
            if user_guess == num_to_guess:
                guesses += 1
                print("You guessed it! You win!\n")
                print(f"It took you {guesses} attempts.\n")
                past_attempts.append(guesses)
                play = input("Would you like to play again? (yes/no)\n")
                
                if play != "yes":
                    print("No worries. Until next time!\n")
                    break
                else:
                    guesses = 0
                    num_to_guess = random.randint(1, 10)
                    show_score(past_attempts)
                    continue
            else:
                # Provide hints
                if int(user_guess) < num_to_guess:
                    print("Not quite. Try a higher number.\n")
                else:
                    print("Nope! Go lower.\n")
        except ValueError as err:
            print("Oh no! That is not a valid number. Try again!\n")
            print(err)
            
# Run only when executed directly
if __name__ == "__main__":
    start_game()
                
    



