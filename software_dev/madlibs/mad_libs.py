# TODO: Add word/symbol art here so that when the program runs, users know what they are playing
print("\n")
print("Welcome to the Mad Libs Generator!")
print("You'll be asked for different words to create a funny story. Let's go!!\n")

def play_game():
    # TODO: Insert tool tips for each word type, so that users can hover over the type and view the definition or example
    # Gather parts of speech
    noun = input("Provide a noun: ")
    p_noun = input("Provide a plural noun: ")
    noun2 = input("Provide a second noun: ")
    place = input("Provide a place: ")
    adjective = input("Provide an adjective (a describing word): ")
    noun3 = input("Provide a third noun: ")


    # Print final MadLibs Story
    print("\n--------------------------")
    print(f"Be kind to your {noun} - footed, {p_noun}")
    print(f"For a duck may be somebody's {noun2},")
    print(f"Be kind to your {p_noun} in {place}")
    print(f"Where the weather is always {adjective}.")
    print(f"You may thing that this is the {noun3}")
    print("Well, it is.")
    print("\n--------------------------")

while True:
    play_game()
    # Ask if user wants to play again
    play_again = input("\nWould you like to play again? Y/N\n").lower()
    if play_again != "y":
        print("\nThanks for playing!\n")
        break
    
    