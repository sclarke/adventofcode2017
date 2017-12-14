from functools import reduce
from itertools import zip_longest
from operator import xor

test_input = [3, 4, 1, 5]
puzzle_input = "129,154,49,198,200,133,97,254,41,6,2,1,255,0,191,108"
puzzle_input_1 = [int(n) for n in puzzle_input.split(',')]


def shuffle_bank(instr, bank_len=256, rounds=64):
    bank = list(range(bank_len))
    pointer = 0
    skip_size = 0
    for _ in range(rounds):
        for length in instr:
            segment = [bank[i % bank_len] for i in range(pointer, pointer + length)]
            for i, n in zip(range(pointer, pointer + length), reversed(segment)):
                bank[i % bank_len] = n
            pointer = (pointer + length + skip_size) % bank_len
            skip_size += 1
    return bank


def solve_1(instr, bank_length=256):
    shuffled_bank = shuffle_bank(instr, bank_len=bank_length, rounds=1)
    return shuffled_bank[0] * shuffled_bank[1]


def encode_input(instr):
    tail = [17, 31, 73, 47, 23]
    return list(instr.encode('ascii')) + tail


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def calc_dense_hash(sparse_input):
    charvals = (reduce(xor, chunk) for chunk in grouper(sparse_input, 16))
    return ''.join(f'{n:02x}' for n in charvals)


if __name__ == "__main__":
    print(solve_1(test_input, bank_length=len(test_input) + 1))
    print(solve_1(puzzle_input_1))

    print(calc_dense_hash(shuffle_bank(encode_input(""))))
    print(calc_dense_hash(shuffle_bank(encode_input("AoC 2017"))))
    print(calc_dense_hash(shuffle_bank(encode_input("1,2,3"))))
    print(calc_dense_hash(shuffle_bank(encode_input("1,2,4"))))
    print(calc_dense_hash(shuffle_bank(encode_input(puzzle_input))))
