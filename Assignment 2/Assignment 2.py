# AUTHOR: SANDER BETZ
# ST. NR: 6070000

# Put imports here
import random

max_guesses : int = 10
guess_num   : int = 0

# Main code
def generate_sequence() -> list:
    # This function may look weird, however it is recursion safe
    # The function checks if all numbers are unique, if it is detected that there are more instances of a number in
    # the sequence, the function calls itself again, and triggers the BREAK. This ensures that when a new sequence
    # is generated, the for loop will not check other numbers in the original sequence. Therefore, if multiple
    # sequences are flawed and one is generated good. The function will collapse due to a chain of breaks in subsequent functions.
    seq = random.sample([i for i in range(1, 7)], 4)
    for i in range(6):
        if seq.count(i) > 1:
            seq = generate_sequence()
            break
    return seq

def init_game() -> list:
    global game_sequence
    game_sequence = generate_sequence()
    print(" *** Mastermind Game! *** ")

    return game_sequence

def ask_guess(cur_guess: int) -> list[int]:
    seq = input(f'Which 4 number sequence do you want to input? \n'
                f'You have {max_guesses - cur_guess} attempts left\n'
                f'Sequence: ')
    if len(seq) != 4:
        print(f'--> You entered {len(seq)} numbers, please input 4 numbers for the game!')
        seq = ask_guess(cur_guess)
    for char in seq:
        if int(char) <= 0 or int(char) > 6:
            print('--> One or more numbers are not valid')
            guess = ask_guess(cur_guess)
    guess = [int(char) for char in seq]

    return guess

def compare_guess(game_sequence: list, guess_sequence: list) -> list:
    guess_states : list = [0, 0, 0, 0]
    for n, key, value in zip([0, 1, 2, 3], guess_sequence, game_sequence):
        if key == value:
            guess_states[n] = 2
        elif key in game_sequence:
            guess_states[n] = 1
        else:
            continue
    return guess_states

def evaluate_guess(states: list) -> None:
    print(f'--> {states.count(0)} not in sequence \n'
          f'--> {states.count(1)} in sequence, wrong place \n'
          f'--> {states.count(2)} in sequence, good location')

def restart_game() -> bool:
    global guess_num
    global game_sequence
    possibilities : list = ['', 'y', 'yes']
    ans = input("Do you want to play another game? Press ENTER, Y, or type YES\n"
                "You entered: ").lower()
    if ans in possibilities:
        game_sequence = generate_sequence()
        guess_num = 0

        return True
    print("--> You chose not to replay. Thank you for playing! Goodbye!")
    return False

def end_game_handling(curr_guess: int, states: list, win_sequence: list) -> bool:
    if curr_guess >= max_guesses:
        print(f'--> Maximum guesses reached, you lose! The sequence was'
              f'{str(win_sequence).replace("[", "").replace("]", "").replace(", ", " ")}')
        return restart_game()
    elif states == [2, 2, 2, 2]:
        print(f'--> Well done! The sequence was indeed '
              f'{str(win_sequence).replace("[", "").replace("]", "").replace(", ", " ")}, '
              f'you win! ')
        return restart_game()
    return True


def main():
    not_guessed : bool = True
    global guess_num
    global game_sequence

    # Initialize the game
    game_sequence = init_game()

    while not_guessed:
        # Ask the user for a guess
        guess = ask_guess(guess_num)

        # Compare the guess to the generated "secret" sequence
        states = compare_guess(game_sequence, guess)

        # Print whatever the previous function returned
        evaluate_guess(states)

        # Game ended?
        guess_num += 1

        # See if the game should end, restart or continue
        not_guessed = end_game_handling(guess_num, states, game_sequence)

if __name__ == '__main__':
    main()