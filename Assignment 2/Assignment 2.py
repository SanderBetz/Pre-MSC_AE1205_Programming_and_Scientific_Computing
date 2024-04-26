# Put imports here
import random
import math

max_guesses = 10

# Main code
def init_game():
    game_sequence = random.sample([i for i in range(1, 7)], 4)

    print(" *** Mastermind Game! *** ")

    return game_sequence

def ask_guess(cur_guess : int) -> list[int]:
    seq = input(f'Which 4 number sequence do you want to input? \n'
                f'You have {max_guesses - cur_guess} attempts left\n'
                f'Sequence: ')
    for char in seq:
        if int(char) <= 0 or int(char) > 6:
            print('--> One or more numbers are not valid')
            guess = ask_guess(cur_guess)
    guess = [int(char) for char in seq]

    return guess

def compare_guess(game_sequence, guess_sequence):
    guess_states = [0, 0, 0, 0]
    for n, key, value in zip([0, 1, 2, 3], guess_sequence, game_sequence):
        if key == value:
            guess_states[n] = 2
        elif key in game_sequence:
            guess_states[n] = 1
        else:
            continue
    return guess_states

def retry_game() -> bool:
    answers = ['', 'y', 'yes']
    ans = input('Would you like to play another game? \n'
                'Press ENTER, Y, or YES to start another')
    if ans.lower() in answers:
        return False
    return True

def evaluate_guess(states: list) -> None:
    print(f'--> {states.count(0)} not in sequence \n'
          f'--> {states.count(1)} in sequence, wrong place \n'
          f'--> {states.count(2)} in sequence, good location')
def main():
    debug_mode = True

    game_sequence = init_game()
    if debug_mode:
        game_sequence = [1, 2, 3, 4]

    not_guessed = True
    guess_num = 0

    while not_guessed:
        guess = ask_guess(guess_num)
        states = compare_guess(game_sequence, guess)
        evaluate_guess(states)


        if not debug_mode:
            print(game_sequence)
            print(guess)
            print(states)

        # MAKE THIS A FUNCTION WITH A BREAK!
        if guess_num >= max_guesses:
            print('--> You Lose!')
            break
        elif states == [2, 2, 2, 2]:
            print('--> You win!')
            break

        not_guessed = retry_game()
        if not not_guessed:
            guess_num = 0

        guess_num += 1





if __name__ == '__main__':
    main()
