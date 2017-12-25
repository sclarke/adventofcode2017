from collections import namedtuple, defaultdict

test_input = '''
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
'''

instr = namedtuple('instruction', ('write_val', 'move_direc', 'next_state'))

test_states = {
    'A': {
        0: instr(1, 1, 'B'),
        1: instr(0, -1, 'B'),
    },
    'B': {
        0: instr(1, -1, 'A'),
        1: instr(1, 1, 'A'),
    }
}

puzzle_states = {
    'A': {
        0: instr(1, 1, 'B'),
        1: instr(0, -1, 'C'),
    },
    'B': {
        0: instr(1, -1, 'A'),
        1: instr(1, 1, 'D'),
    },
    'C': {
        0: instr(1, 1, 'A'),
        1: instr(0, -1, 'E'),
    },
    'D': {
        0: instr(1, 1, 'A'),
        1: instr(0, 1, 'B'),
    },
    'E': {
        0: instr(1, -1, 'F'),
        1: instr(1, -1, 'C'),
    },
    'F': {
        0: instr(1, 1, 'D'),
        1: instr(1, 1, 'A'),
    },
}


def run_machine(states, initial_state='A', steps=6):
    tape = defaultdict(int)
    pointer = 0
    state = initial_state
    for _ in range(steps):
        instruction = states[state][tape[pointer]]
        tape[pointer] = instruction.write_val
        pointer += instruction.move_direc
        state = instruction.next_state
    return sum(tape.values())


print(run_machine(test_states))
print(run_machine(puzzle_states, steps=12173597))
