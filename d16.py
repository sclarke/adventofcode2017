from functools import partial, lru_cache
from string import ascii_lowercase

test_input = "s1,x3/4,pe/b".split(',')
with open('d16_input.txt') as f:
    puzzle_input = f.read().strip().split(',')


class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not tuple(tuple(arg) for arg in args) in self.memo:
            self.memo[tuple(tuple(arg) for arg in args)] = self.f(*args)
        return self.memo[tuple(tuple(arg) for arg in args)]


@Memoize
def choreograph(positions, inp):
    for dance_move in inp:
        positions = perform_move(positions, dance_move)
    return positions


def spin_move(positions, index):
    index = int(index)
    return positions[-index:] + positions[:-index]


def exchange_move(positions, index_a, index_b):
    index_a, index_b = (int(n) for n in (index_a, index_b))
    positions[index_a], positions[index_b] = positions[index_b], positions[index_a]
    return positions


def partner_move(positions, name_a, name_b):
    index_a, index_b = positions.index(name_a), positions.index(name_b)
    return exchange_move(positions, index_a, index_b)


def perform_move(positions, dance_move):
    move, args = dance_move[0], dance_move[1:]

    moves = {
        's': partial(spin_move, positions),
        'x': partial(exchange_move, positions),
        'p': partial(partner_move, positions),
    }

    args = args.split('/')
    return moves[move](*args)


print(''.join(choreograph(list(ascii_lowercase[:5]), test_input)))
print(''.join(choreograph(list(ascii_lowercase[:16]), puzzle_input)))

ordering = list(ascii_lowercase[:16])
for _ in range(1_000_000_000):
    ordering = choreograph(ordering, puzzle_input)
print(''.join(ordering))
