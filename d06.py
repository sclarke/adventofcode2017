

test_input = [int(x) for x in "0    2   7   0".split()]
puzzle_input = [int(x) for x in "5	1	10	0	1	7	13	14	3	12	8	10	7	12	0	6".split()]


def find_imax(iterable):
    imax = 0
    maxseen = 0
    for index, val in enumerate(iterable):
        if val > maxseen:
            imax, maxseen = index, val
    return imax


def redistribute(banks):
    target_index = find_imax(banks)
    blocks, banks[target_index] = banks[target_index], 0
    for i in range(target_index + 1, target_index + blocks + 1):
        banks[i % len(banks)] += 1
    return tuple(banks)


def calc_cycles(banks):
    steps = 0
    banks_history = [tuple(banks)]
    while True:
        new_banks = redistribute(banks)
        steps += 1
        if new_banks in banks_history:
            break
        else:
            banks_history.append(new_banks)
    return steps, len(banks_history) - banks_history.index(new_banks)


print(calc_cycles(test_input))
print(calc_cycles(puzzle_input))
