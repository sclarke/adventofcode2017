from collections import defaultdict
from string import ascii_letters, digits

from d10 import calc_dense_hash, shuffle_bank, encode_input

test_input = "flqrgnkx"
puzzle_input = "jzgqcdpd"


def base_n(num, b=36, numerals=digits + ascii_letters + '@#'):
    return ((num == 0) and numerals[0]) or (base_n(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


def get_hashes(key, start=0, end=128):
    hash_inputs = [f'{key}-{n:d}' for n in range(start, end)]
    hashes = [calc_dense_hash(shuffle_bank(encode_input(hi))) for hi in hash_inputs]
    return [f'{int(x, base=16):0128b}' for x in hashes]


def get_total_used(key):
    binary_hashes = get_hashes(key)
    return sum(s.count('1') for s in binary_hashes)


def neighbors(cx, cy):
    return [
        (cx, cy - 1), (cx - 1, cy),
        (cx, cy + 1), (cx + 1, cy),
    ]


def get_regions_count(key, debug_print=False):
    binary_hashes = get_hashes(key)
    region_table = defaultdict(int)

    region_number = 0

    def _already_seen(xx, yy):
        return region_table[xx, yy] > 0

    def _is_used(xx, yy):
        return binary_hashes[yy][xx] == "1" if xx in range(128) and yy in range(128) else False

    def _is_used_and_not_already_seen(*loc):
        return _is_used(*loc) and not _already_seen(*loc)

    for y, row in enumerate(binary_hashes):
        for x, col in enumerate(row):
            if _is_used_and_not_already_seen(x, y):
                region = {(x, y)}
                region_number += 1
                region_table[x, y] = region_number
                while region:
                    region = {neighbor_loc for loc in region for neighbor_loc in neighbors(*loc) if
                              _is_used_and_not_already_seen(*neighbor_loc)}
                    for xn, yn, in region:
                        region_table[xn, yn] = region_number

            if debug_print:
                region_str = base_n(region_table[x, y]) if region_table[x, y] > 0 else "."
                print(f'{region_str:^3s}', end="")
        if debug_print:
            print()

    return region_number


if __name__ == "__main__":
    print(get_total_used(test_input))
    print(get_total_used(puzzle_input))

    print(get_regions_count(test_input, debug_print=True))
    print(get_regions_count(puzzle_input))
