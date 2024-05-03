# Put imports here

alphabet = list('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split(' '))

def normalize(og_list: list) -> list:
    summed = sum(og_list)
    new_list = []
    for item in og_list:
        new_list.append(item / summed)
    return new_list

def normal_frequencies() -> list:
    char_lst = {}
    with open(f'letter frequencies/ch-freq-en.txt', 'r') as file:
        for line in file.readlines():
            char_lst[line.split('	')[0]] = float(line.split('	')[1].replace(r'\n', ''))

    filtered = filter_item(char_lst)
    return filtered

def read_frequencies(file_name: str) -> list:
    char_lst = {default_char : 0 for default_char in alphabet}
    char_num = 0
    with open(f'cyphers/{file_name}.txt', 'r') as file:
        for char in file.read():
            if (n:= char.upper()) in alphabet:
                char_lst[n] += 1
                char_num += 1
    new_chars = {}
    for key, val in char_lst.items():
        new_chars[key] = val / char_num
    filtered = filter_item(new_chars)
    return filtered

def filter_item(char_lst: dict) -> list:
    char_lst = dict(sorted(char_lst.items(), key=lambda x: x[0]))
    return normalize(list(char_lst.values()))

def calculate_difference(shift: int, default_freqs: list, read_freqs: list) -> float:
    difference = 0
    for num, (default, read) in enumerate(zip(default_freqs, read_freqs)):
        if (num + shift) >= 26:
            read = read_freqs[num + shift - 26]
        else:
            read = read_freqs[num + shift]

        difference += abs(default - read)
    return difference

def shift_alphabet(shift: int) -> dict:
    shifted_alphabet = {}
    for index, letter in enumerate(alphabet):
        try:
            shifted_alphabet[letter] = alphabet[index + shift]
        except:
            shifted_alphabet[letter] = alphabet[index + shift - 26]
    return shifted_alphabet

def decypher(path: str, shifted: dict, only_first_characters: int=0) -> None:
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
    if only_first_characters != 0:
        print((''.join(final_text))[0:only_first_characters])
    else:
        print((''.join(final_text)))

# Main code
def main(path):
    # path = 'secret0'
    default_freqs = normal_frequencies()
    read_freqs = read_frequencies(path)

    options = {i : 0. for i in range(26)}
    for i in options.keys():
        options[i] = calculate_difference(i, default_freqs, read_freqs)

    # print(options)
    pred_shift = 26 - list(dict(sorted(options.items(), key=lambda x:x[1])))[0]

    alphabet_shifted = shift_alphabet(pred_shift)

    decypher(path, alphabet_shifted, only_first_characters=50)

if __name__ == '__main__':
    paths = ['testdata', 'secret0', 'secret1', 'secret2', 'secret3', 'secret4', 'secret5', 'secret6']
    for i in paths:
        print(f'\n'
              f'--> Now decyphering: {i}')
        main(i)