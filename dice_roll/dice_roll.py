import random
import os

def play():
    name = input("Enter your name: ")
    play = input(f"Hi {name}! Would you like to play Dice Roll? (yes/no)\n").lower()
    

    if play != "yes":
        print("Ah bummer. Maybe next time.")
    else:
        # Game loop
        while play == "yes":
            os.system("clear")
            num_to_roll = int(input(f"Welcome {name}! Select how many dice you'd like to roll (1 or 2): "))
            if num_to_roll < 1 or num_to_roll > 2:
                num_to_roll = input("Oops! Your input was invalid. Choose either 1 or 2 dice to roll.\n")
            if num_to_roll == 1:
                dice_value = random.randint(1, 6)
                print(f"You rolled a {dice_value}.")
            else:
                dice_value_1 = random.randint(1, 6)
                dice_value_2 = random.randint(1, 6)
                dice_value_total = dice_value_1 + dice_value_2
                print(f"First die: {dice_value_1}\n"
                      f"Second die: {dice_value_2}\n"
                      f"You rolled a total score of {dice_value_total}.\n")
            
            play = input("Play again? (yes/no):\n")
            if play != "yes":
                print("Thank you for playing!")
                exit()

if __name__ == "__main__":
    play()
            
        
    