

# part one initially solved by browsing through the grid at https://www.alpertron.com.ar/ULAM.HTM
# (not super proud of that!, but 368078 is at (303, -68)

from collections import defaultdict
from functools import lru_cache


@lru_cache(maxsize=500_000)
def get_xy_coord(n):
    """compute the xy coordinate given an index"""
    if n < 1:
        raise ValueError
    elif n == 1:
        return 0, 0
    elif n == 2:
        return 1, 0
    else:
        x, y = get_xy_coord(n-1)
        if abs(x) > abs(y):
            # spiral is going up the right side or down the left side
            if x >= 0:
                # spiral is going up the right
                return (x, y + 1) if (y < x) else (x - 1, y)
            else:
                # spiral is going down the left
                return (x, y - 1) if (y > x) else (x + 1, y)
        else:
            # spiral is going left on top or right on bottom
            if y >= 0:
                # spiral is going left on top
                return (x - 1, y) if (x > -y) else (x, y - 1)
            else:
                # spiral is going right on bottom (y is negative)
                return (x + 1, y)  # keep going right past x == -y so no if/else needed


def manhattan_dist(coordinates):
    """calculates manhattan distance in multiple dimensions"""
    return sum(abs(coordinate) for coordinate in coordinates)


def get_neighbors(a, b):
    return [
        (a + 1, b    ),  # →
        (a + 1, b + 1),  # ↗
        (a    , b + 1),  # ↑
        (a - 1, b + 1),  # ↖
        (a - 1, b    ),  # ←
        (a - 1, b - 1),  # ↙
        (a    , b - 1),  # ↓
        (a + 1, b - 1),  # ↘
    ]


if __name__ == "__main__":

    mygrid = dict()
    puzzle_input = 368078

    for i in range(1, puzzle_input + 1):
        mygrid[i] = get_xy_coord(i)

    for val in (1, 12, 23, 1024, puzzle_input):
        print(manhattan_dist(mygrid[val]))

    # part one works!

    mygrid_values = defaultdict(int)
    mygrid_values[(0, 0)] = 1

    max_val = 0
    index = 1
    while max_val < puzzle_input:
        index = index + 1
        x, y = mygrid[index]
        mygrid_values[x, y] = sum(mygrid_values[xx, yy] for xx, yy in get_neighbors(x, y))
        max_val = max(max_val, mygrid_values[x, y])

    for val in (1, 2, 3, 4, 5, index):
        print(mygrid[val], mygrid_values[mygrid[val]])
