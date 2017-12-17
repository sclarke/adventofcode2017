from collections import deque

test_input = 3
puzzle_input = 359


def build_buffer(step_size, steps=2017):
    buffer = deque((0, ))
    for i in range(1, steps+1):
        buffer.rotate(-step_size)
        buffer.append(i)
    return buffer


def get_short_circuit_values(step_size, steps=2017):
    buf = build_buffer(step_size, steps)
    after_last_inserted_value = buf[0]
    buf.rotate(-buf.index(0)-1)
    after_zero_value = buf[0]
    return after_last_inserted_value, after_zero_value


# Part 1
print(get_short_circuit_values(test_input)[0])
print(get_short_circuit_values(puzzle_input)[0])

# Part 2
print(get_short_circuit_values(puzzle_input, steps=50_000_000)[1])
