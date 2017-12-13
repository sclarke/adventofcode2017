
def parse_line(line):
    return tuple(int(n) for n in line.split(': '))


test_input = """
0: 3
1: 2
4: 4
6: 4""".strip().splitlines()
test_input = [parse_line(line) for line in test_input]

with open('d13_input.txt') as f:
    puzzle_input = [parse_line(line) for line in f.readlines()]


def is_caught(layer, depth, start_time=0):
    period = 2 * (depth - 2) + 2
    return (layer + start_time) % period == 0


def calc_score(inp, start_time=0, strict=False):
    score = 0
    for layer, depth in inp:
        caught = is_caught(layer, depth, start_time)
        assert not (strict and caught)  # if strict mode, raise AssertionError if caught
        layer_score = layer*depth if caught else 0
        score += layer_score
    return score


def get_delay(inp):
    start = 0
    while True:
        try:
            calc_score(inp, start, strict=True)
        except AssertionError:
            start += 1
        else:
            break
    return start


print(calc_score(test_input))
print(calc_score(puzzle_input))

print(get_delay(test_input))
print(get_delay(puzzle_input))
