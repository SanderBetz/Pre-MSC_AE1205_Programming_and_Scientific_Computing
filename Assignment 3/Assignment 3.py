# Put imports here
import math

# Main code
def read_file(path: str) -> tuple[dict, int]:
    letters       : dict  = {}
    letter_length : int   = 0
    with open(f'cyphers/{path}.txt', 'r') as file:
        for n, letter in enumerate(file.read().replace(' ', '')):
            alphabet = 'ABCDEFGHIJKLMNOPQRTSUVWXYZ'
            if (letter := letter.upper()) not in letters.keys():
                letters[letter] = 0
            else:
                letters[letter] += 1
            if n > letter_length:
                letter_length = n
    return (letters, n)

def load_letter_freq() -> dict:
    ...

def get_letter_freq(letters: dict, length: int):
    letter_freqs : dict = {}
    for letter, num_counted in letters.items():
        letter_freqs[letter] = num_counted / length
    return letter_freqs

def compare_letter_freq():
    ...

def decypher(shift: int):
    alphabet = 'ABCDEFGHIJKLMNOPQRTSUVWXYZ'
    ...


def main():
    letter_set, letter_length = read_file('secret0')
    letter_freqs = get_letter_freq(letter_set, letter_length)
    print(letter_freqs)
    print(list(letter_set.keys()))

    for (char, num), freq in zip(letter_set.items(), letter_freqs.values()):
        print(char, num, f'{round(freq*100, 2)}%')



if __name__ == '__main__':
    main()
