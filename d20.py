from collections import Counter
from re import compile
from d03 import manhattan_dist

test_input1 = """
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0> 
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
""".strip().splitlines()

test_input2 = """
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
""".strip().splitlines()

with open('d20_input.txt') as f:
    puzzle_input = [line.strip() for line in f.readlines()]


def parse_input(inp):
    coord_pattern = compile('[pva]=<(?P<x>[- \d]+),(?P<y>[- \d]+),(?P<z>[- \d]+)>')
    all_lines = []
    for line in inp:
        pva_components = line.strip().split(', ')
        pva_parsed = []
        for xyz in pva_components:
            numbers = tuple(int(n.strip()) for n in coord_pattern.match(xyz).groups())
            pva_parsed.append(numbers)
        all_lines.append(pva_parsed)
    return all_lines


def get_min_accel(state):
    min_accel = min(manhattan_dist(a) for p, v, a in state)
    return [(i, (p, v, a)) for i, (p, v, a) in enumerate(state) if manhattan_dist(a) == min_accel]


def get_min_dist(state):
    indices, trimmed_state = zip(*get_min_accel(state))
    far_future_state = run_sim(trimmed_state)
    distances = [manhattan_dist(p) for p, v, a in far_future_state]
    return indices[distances.index(min(distances))]


def step_sim(state): return [step_particle_state(*particle) for particle in state]


def step_particle_state(p, v, a):
    new_a = tuple(a)
    new_v = tuple(m + n for m, n in zip(v, new_a))
    new_p = tuple(l + m for l, m in zip(p, new_v))
    return new_p, new_v, new_a


def remove_collisions(state):
    all_positions = Counter([p for p, v, a in state])
    crowded_positions = {p for p, count in all_positions.most_common() if count > 1}
    return [(p, v, a) for (p, v, a) in state if p not in crowded_positions]


def run_sim(state, steps=100):
    for _ in range(steps):
        state = remove_collisions(step_sim(state))
    return state


print('Part 1 Test:', get_min_dist(parse_input(test_input1)))
print('Part 1 Puzzle:', get_min_dist(parse_input(puzzle_input)))

print('Part 2 Test:', len(run_sim(parse_input(test_input2))))
print('Part 2 Puzzle:', len(run_sim(parse_input(puzzle_input))))
