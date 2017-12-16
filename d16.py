from collections import deque
from copy import deepcopy
from string import ascii_lowercase


def spin_move(positions, index):
    positions.rotate(index)


def exchange_move(positions, index_a, index_b):
    positions[index_a], positions[index_b] = positions[index_b], positions[index_a]


def partner_move(positions, name_a, name_b):
    index_a, index_b = positions.index(name_a), positions.index(name_b)
    positions[index_a], positions[index_b] = name_b, name_a


def parse_input(input_str):
    moves = {
        's': spin_move,
        'x': exchange_move,
        'p': partner_move,
    }

    def parse_move(dance_move):
        move, args = dance_move[0], dance_move[1:]
        args = args.split('/')
        if move in 'sx':
            args = tuple(int(n) for n in args)
        return moves[move], args

    return tuple(parse_move(dance_move) for dance_move in input_str)


test_input = parse_input("s1,x3/4,pe/b".split(','))
with open('d16_input.txt') as f:
    puzzle_input = parse_input(f.read().strip().split(','))


class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        frozen_positions = ''.join(args[0])
        if frozen_positions not in self.memo:
            self.memo[frozen_positions] = self.f(*args)
        return deepcopy(self.memo[frozen_positions])


@Memoize
def choreograph(positions, inp):
    for move, args in inp:
        move(positions, *args)
    return positions


print(''.join(choreograph(deque(ascii_lowercase[:5]), test_input)))
print(''.join(choreograph(deque(ascii_lowercase[:16]), puzzle_input)))

ordering = deque(ascii_lowercase[:16])
for _ in range(120):
    print(_, ''.join(ordering))
    ordering = choreograph(ordering, puzzle_input)

# It looks like the whole cycle repeats every 60 entries. Since 1_000_000_000 % 60 == 40, entry number 40 is the answer.
# The code is fast enough with the memoization that it should only take about an hour to run outright.
