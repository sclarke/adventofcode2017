from itertools import product
from math import sqrt

seed_pattern = '.#./..#/###'

test_input = '''
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
'''.strip().splitlines()

with open('d21_input.txt') as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def parse_input(inp): return dict(tuple(line.split(' => ')) for line in inp)


def unpack_pattern(pat): return pat.split('/')


def pack_pattern(pat): return '/'.join(pat)


def subdivide(pat):
    sub_el_size = 2 if len(pat) % 2 == 0 else 3 if len(pat) % 3 == 0 else 1
    sub_elements = []
    for x, y in product(range(0, len(pat), sub_el_size), repeat=2):
        sub_elements.append([pat[x + i][y:y + sub_el_size] for i in range(sub_el_size)])
    return sub_elements


def do_rot(pat, rot):
    if rot == 0:
        return pat
    elif rot == 1:
        return (''.join(s) for s in zip(*reversed(pat)))
    elif rot == 2:
        return (s[::-1] for s in pat[::-1])
    elif rot == 3:
        return reversed([''.join(s) for s in zip(*pat)])
    else:
        raise ValueError


def do_flip(pat, flip=True): return [''.join(reversed(row)) for row in pat] if flip else pat


def transform(pat): return (do_rot(do_flip(pat, flip), rot) for flip, rot in product([False, True], range(4)))


def enhance_pattern(pat, enhancements):
    for pattern in transform(pat):
        try:
            return unpack_pattern(enhancements[pack_pattern(pattern)])
        except KeyError:
            pass
    else:
        raise KeyError


def join_patterns(patterns):
    # reshape the list of patterns into rows/columns of patterns
    grouped_patterns = zip(*[iter(patterns)]*int(sqrt(len(patterns))))
    return [''.join(row) for major_row in grouped_patterns for row in zip(*major_row)]


def iterate_patterns(pat, enhancements, steps=2):
    pat = unpack_pattern(pat)
    for _ in range(steps):
        patterns = [enhance_pattern(pat, enhancements) for pat in (subdivide(pat))]
        pat = join_patterns(patterns)
    return pack_pattern(pat)


print(iterate_patterns(seed_pattern, parse_input(test_input), steps=2).count('#'))
print(iterate_patterns(seed_pattern, parse_input(puzzle_input), steps=5).count('#'))
print(iterate_patterns(seed_pattern, parse_input(puzzle_input), steps=18).count('#'))
