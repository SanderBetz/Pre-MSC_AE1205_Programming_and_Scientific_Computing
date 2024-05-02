

x = [3, 2, 2, 2]
g = [1, 2, 3, 4]
states = [0, 0, 0, 0]

for n, i, j in zip([0, 1, 2, 3], x, g):
    if i == j:
        states[n] = 2
    elif i in g:
        states[n] = 1

print(f"you've entered {states.count(2)} good inputs, good locations")
print(f"you've entered {states.count(1)} good inputs, wrong locations")
print(f"you've entered {states.count(0)} wrong inputs")

if states == [2, 2, 2, 2]:
    print('you win!')

