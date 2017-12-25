from copy import deepcopy
from operator import itemgetter

test_input = """
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10""".strip().splitlines()

with open('d24_input.txt') as f:
    puzzle_input = f.readlines()


def parse_input(inp):
    return [pair.strip().split('/') for pair in inp]


def extend_chains(all_pairs, match_value):
    all_chains = []
    for pair in all_pairs:
        if match_value in pair:
            all_chains.append([[pair]])
            next_match = deepcopy(pair)
            next_match.remove(match_value)
            pairs = deepcopy(all_pairs)
            pairs.remove(pair)
            all_chains.append([[pair] + chain for chains in extend_chains(pairs, *next_match) for chain in chains])
    return all_chains


# TODO: why do I need both of these functions?
def build_chains(all_pairs, match_value='0'):
    all_chains = []
    for pair in all_pairs:
        if match_value in pair:
            all_chains.append([pair])
            next_match = deepcopy(pair)
            next_match.remove(match_value)
            pairs = deepcopy(all_pairs)
            pairs.remove(pair)
            all_chains += [[pair] + chain for chains in extend_chains(pairs, *next_match) for chain in chains]
            # for chains in build_chains(pairs, *next_match):
            #     for chain in chains:
            #         all_chains.append([[pair] + chain])

    return all_chains


def compute_strength(chain):
    return sum(int(n) for pair in chain for n in pair)


def get_best_chain(chains):
    lengths_strengths = [(len(chain), compute_strength(chain)) for chain in chains]
    return sorted(sorted(lengths_strengths, key=itemgetter(1), reverse=True), key=itemgetter(0), reverse=True)[:3]


for chain in build_chains(parse_input(test_input)):
    print(compute_strength(chain), len(chain), chain)

print('Test:', get_best_chain(build_chains(parse_input(test_input))))
# print('Test:', get_best_chain(extend_chains('0', parse_input(test_input))))
# print('Puzzle:', get_best_chain(build_chains(parse_input(puzzle_input))))
