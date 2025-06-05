import random
from colorama import init, Fore, Back, Style

print("Die sal dadelik uitgevoer word.")


# Hierdie skep n funkie wat jy enige tyd kan roep
# funksies word nie dadelik uitgevoer nie.
def guess_the_number():
    # Step 1: Generate a random number between 1 and 100
    number_to_guess = random.randint(1, 100)
    number_of_attempts = 0
    guessed = False

    print("Welcome to the 'Guess the Number' game!")
    print("I'm thinking of a number between 1 and 100.")

    # Step 2: Game loop
    minn = 0
    maxx = 100
    while not guessed:
        # Step 3: Ask the player to guess the number
        try:
            guess = int(input("Take a guess: "))
            number_of_attempts += 1

            # Step 4: Provide feedback
            if guess < number_to_guess:
                minn = max(minn,guess)
                print(Fore.GREEN +"Your guess is too low. (Min", minn, "Max", maxx,")")
            elif guess > number_to_guess:
                maxx = min(maxx, guess)
                print(Fore.RED + "Your guess is too high. (Min", minn, "Max", maxx,")")
            else:
                guessed = True
                print(Fore.CYAN + f"Good job! You guessed the number in {number_of_attempts} attempts.")
        except ValueError:
            print(Fore.MAGENTA + "Please enter a valid number.")


# Hier is nog n funksie.
def printMyMessage(message, color):
    print(color+ message + Style.RESET_ALL)


# Loop jou funksies in die volgorde
guess_the_number()
printMyMessage('Thank you for playing ', Fore.LIGHTRED_EX)
printMyMessage('All rights reserved LJ Software 2025 ©', Fore.BLUE)
