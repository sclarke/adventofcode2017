from collections import defaultdict
from copy import deepcopy

test_input = '''
..#
#..
...
'''.strip().splitlines()

with open('d22_input.txt') as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def build_grid(inp):
    """represent the infinite grid with a defaultdict so that the coordinates can grow arbitrarily."""
    size = len(inp)
    grid = defaultdict(int)

    # Could probably un-nest this with itertools.product and reversing the input, but this function doesn't get called
    #  enough to matter
    for j, y in enumerate(range(int((size - 1) / 2), -int((size - 1) / 2) - 1, -1)):
        for i, x in enumerate(range(-int((size - 1) / 2), int((size - 1) / 2) + 1)):
            grid[(x, y)] = 1 if inp[j][i] == '#' else 0
    return grid


def move(new_direction, x, y):
    if new_direction == 0:
        x += 1
    elif new_direction == 1:
        y += 1
    elif new_direction == 2:
        x -= 1
    elif new_direction == 3:
        y -= 1
    return x, y


def step(grid, direc, coord, part2_mode):
    next_direction = {0: 1, 1: 0, 2: -1, 3: 2} if part2_mode else {1: -1, 0: 1}
    new_direction = (direc + next_direction[grid[coord]]) % 4
    grid[coord] = (grid[coord] + 1) % 4 if part2_mode else grid[coord] ^ 1
    new_coord = move(new_direction, *coord)
    return grid[coord], new_direction, new_coord


def iterate(grid, steps=10_000, part2_mode=False):
    grid = deepcopy(grid)
    infected_value = 1

    if part2_mode:
        for k in grid:
            grid[k] *= 2
        infected_value = 2

    new_infections = 0

    direction = 1
    coord = (0, 0)
    for _ in range(steps):
        action, direction, coord = step(grid, direction, coord, part2_mode)
        if action == infected_value:
            new_infections += 1
    return new_infections


print(iterate(build_grid(test_input)))
print(iterate(build_grid(puzzle_input)))
print(iterate(build_grid(test_input), steps=100, part2_mode=True))
print(iterate(build_grid(puzzle_input), steps=10_000_000, part2_mode=True))
