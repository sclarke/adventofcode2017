from collections import defaultdict
import math

with open('d23_input.txt') as f:
    puzzle_input = [line.strip().split() for line in f.readlines()]


def run_program(instructions, part2_mode=False):
    registers = defaultdict(int)
    if part2_mode:
        registers['a'] = 1

    pointer = 0
    mul_count = 0

    def get_value(n):
        return int(n) if not n.isalpha() else registers[n]

    def cpy(x, y):
        registers[x] = get_value(y)

    def sub(x, y):
        registers[x] -= get_value(y)

    def mul(x, y):
        registers[x] *= get_value(y)

    def jnz(x, y):
        nonlocal pointer
        if (get_value(x)) != 0:
            pointer += get_value(y)
        else:
            pointer += 1

    commands = dict(set=cpy, sub=sub, mul=mul, jnz=jnz)

    while 0 <= pointer < len(instructions):
        try:
            cmd, *par = instructions[pointer]
        except IndexError:
            break

        # this is interesting if we hack the input values to smaller/manageable numbers
        if part2_mode and pointer == 24:
            print(registers)
        commands[cmd](*par)

        if cmd != 'jnz':
            pointer += 1

        if not part2_mode and cmd == 'mul':
            mul_count += 1

    return mul_count


def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n)) + 1, 2))


print('Part 1:', run_program(puzzle_input))
# only useful if the program is hacked to be faster (i.e., smaller register values in the input file)
# print(run_program(puzzle_input, part2_mode=True))


# with smaller numbers in the input registers, the inconsistent increment of register h becomes apparent.
# Looks like h doesn't increment for each value of b (stepping by 17) when b is prime.
# for n in range(81, 1781, 17):
#     print(n, is_prime(n))


register_b = 81 * 100 + 100_000  # puzzle_input[0], puzzle_input[4], puzzle_input[5]
register_c = register_b + 17_000  # puzzle_input[6], puzzle_input[7]
step_size = 17  # puzzle_input[30]
print('Part 2:', sum(not is_prime(n) for n in range(register_b, register_c + 1, step_size)))
