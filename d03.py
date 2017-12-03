

# part one initially solved by browsing through the grid at https://www.alpertron.com.ar/ULAM.HTM
# (not super proud of that!, but 368078 is at (303, -68)

from collections import defaultdict
from functools import lru_cache

mygrid = dict()


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
                return (x + 1, y)# if (x < -y) else (x, y + 1)


for i in range(1, 368079):
    mygrid[i] = get_xy_coord(i)

def manhattan_dist(coords):
    return sum(abs(n) for n in coords)

for n in (1, 12, 23, 1024, 368078):
    print(manhattan_dist(mygrid[n]))

# part one works!
