from re import match
from operator import ne, lt, le, eq, gt, ge
from collections import defaultdict

test_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".splitlines()

with open('d08_input.txt') as f:
    puzzle_input = f.readlines()


def parse_line(line):
    parts = match('(?P<reg>\w+) (?P<op>(inc|dec)) (?P<count>-?\d+) if '
                  '(?P<test_reg>\w+) (?P<test>\W{1,2}) (?P<test_val>-?\d+)', line).groupdict()

    parts['count'] = int(parts['count'])
    parts['test_val'] = int(parts['test_val'])

    return parts


def perform_test(reg, test_op, val, reg_table):
    ops = {"==": eq, "!=": ne, ">=": ge, "<=": le, ">": gt, "<": lt}
    return ops[test_op](reg_table[reg], val)


def perform_op(reg, operation, val, reg_table):
    ops = {'inc': +1, 'dec': -1}
    reg_table[reg] += ops[operation]*val


def compute_program(inp):
    registers = defaultdict(int)
    instant_max = 0
    for line in inp:
        line_parts = parse_line(line)
        if perform_test(line_parts['test_reg'], line_parts['test'], line_parts['test_val'], registers):
            perform_op(line_parts['reg'], line_parts['op'], line_parts['count'], registers)
            instant_max = max(instant_max, max(registers.values()))

    return max(registers.values()), instant_max


print(compute_program(test_input))
print(compute_program(puzzle_input))
