from itertools import islice

# Puzzle input
# Generator A starts with 722
# Generator B starts with 354


def generator(start, cofactor, divisor=2147483647, out_mask=1):
    prev = start
    while True:
        prev = (prev * cofactor) % divisor
        if prev % out_mask == 0:
            yield prev


def cycle_generators(a_start, b_start, picky=False):
    a_mask = 4 if picky else 1
    b_mask = 8 if picky else 1

    gen_a = generator(a_start, cofactor=16807, out_mask=a_mask)
    gen_b = generator(b_start, cofactor=48271, out_mask=b_mask)

    mask = 2 ** 16
    run_count = 5_000_000 if picky else 40_000_000
    return sum(a % mask == b % mask for a, b in islice(zip(gen_a, gen_b), run_count))


print(cycle_generators(a_start=65, b_start=8921))
print(cycle_generators(a_start=722, b_start=354))

print(cycle_generators(a_start=65, b_start=8921, picky=True))
print(cycle_generators(a_start=722, b_start=354, picky=True))
