
sequence = [1, 2, 3, 4]
guesses = [2, 5, 6, 4]

list_state = [0, 0, 0, 0]

for key, value in zip(guesses, sequence):
    if key == value:
        state = "In sequence, good location"
    elif key in sequence:
        state = "In sequence, wrong location"
    else:
        state = "Not in sequence"

    print(key, value, state)

