# Put imports here
import math

alphabet = list('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' '))

# Main code
def read_file(path: str) -> tuple[dict, int]:
    letter_length : int   = 0
    letters: dict = {f'{let}': 0 for let in alphabet}
    with open(f'cyphers/{path}.txt', 'r') as file:
        for n, letter in enumerate(file.read().replace(' ', '')):
            if (letter:= letter.upper()) in alphabet:
                letters[letter] += 1
                n += 1
    return (letters, n)

def normalize_freqs(d: dict):
    total = sum(d.values())
    for key, val in d.items():
        d[key] = val / total
    return d

def load_letter_freq() -> dict:
    with open('letter frequencies/ch-freq-en.txt', 'r') as file:
        freqs = {}
        for line in file.readlines():
            first, second = line.split('	')
            freqs[first] = float(str(second).replace(r'\n', ''))

    freqs = normalize_freqs(freqs)
    return dict(sorted(freqs.items(), key=lambda x:x[0]))

def get_letter_freq(letters: dict, length: int):
    letter_freqs : dict = {}
    for letter, num_counted in letters.items():
        letter_freqs[letter] = round((num_counted / length)*100, 2)
    letter_freqs = normalize_freqs(letter_freqs)
    return dict(sorted(letter_freqs.items(), key=lambda x:x[0]))

def compare_letter_freq(ref_freqs: dict, read_freqs: dict) -> int:
    diff_index = {}
    print(ref_freqs)
    print(read_freqs)
    diff = 0
    for shift in range(26):
        for n, (key, value) in enumerate(ref_freqs.items()):
            diff = 0
            try:
                # print(abs(value - read_freqs[alphabet[n + shift]]))
                diff += abs(value - read_freqs[alphabet[n + shift]])
            except:
                # print(abs(value - read_freqs[alphabet[n + shift - 26]]))
                diff += abs(value - read_freqs[alphabet[n + shift - 26]])
            diff_index[shift] = diff

    k = list(dict(sorted(diff_index.items(), key=lambda x:x[1])))[0]
    print(k)

    return k


def shift_alphabet(shift: int) -> dict:
    shifted_alphabet = {}
    for index, letter in enumerate(alphabet):
        try:
            shifted_alphabet[letter] = alphabet[index + shift]
        except:
            shifted_alphabet[letter] = alphabet[index + shift - 26]
    return shifted_alphabet

def decypher(path: str, shifted: dict):
    final_text = []
    with open(f'cyphers/{path}.txt', 'r') as file:
        for letter in file.read():
            if (n:=letter.upper()) not in alphabet:
                final_text.append(str(letter))
            else:
                if letter.isupper():
                    final_text.append(shifted[n])
                else:
                    final_text.append((shifted[n]).lower())

    print((''.join(final_text))[0:30])

def main():
    text = 'secret6'
    freqs = load_letter_freq()
    letter_set, letter_length = read_file(text)
    letter_freqs = get_letter_freq(letter_set, letter_length)
    shift = compare_letter_freq(freqs, letter_freqs)
    print(shift)

    for shifttemp in range(26):
        shifted_alphabet = shift_alphabet(shifttemp)
        print(shifttemp)
        decypher(text, shifted_alphabet)

if __name__ == '__main__':
    main()