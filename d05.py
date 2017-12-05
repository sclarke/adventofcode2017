from copy import deepcopy

test_input = [int(x) for x in '0 3 0 1 -3'.split()]

with open('d05_input.txt') as f:
    puzzle_input = [int(x) for x in f.readlines()]


def calc_offset(offset):
    """Part 1 offset is incremented by 1 after it's used"""
    return offset + 1


def calc_offset_2(offset):
    """Part 2 offset is incremented by 1 after it's used unless it's decremented"""
    return offset - 1 if offset >= 3 else offset + 1


def count_steps(jump_list, pointer=0, new_offset=calc_offset):
    step_count = 0
    while 0 <= pointer < len(jump_list):
        jump_list[pointer], pointer = new_offset(jump_list[pointer]), pointer + jump_list[pointer]
        step_count += 1
    return step_count


print('test_input', count_steps(deepcopy(test_input)))
print('puzzle_input', count_steps(deepcopy(puzzle_input)))

print('test_input_2', count_steps(deepcopy(test_input), new_offset=calc_offset_2))
print('puzzle_input_2', count_steps(deepcopy(puzzle_input), new_offset=calc_offset_2))
