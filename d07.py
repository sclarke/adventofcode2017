from re import match
from collections import Counter

test_input = """
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
""".strip().splitlines()

with open('d07_input.txt') as f:
    puzzle_input = f.readlines()


def parse_input(line):
    parts = match('(?P<name>\w+) \((?P<weight>\d+)\)(?: -> (?P<subs>.*))?', line).groupdict()
    if parts['subs']:
        parts['subs'] = parts['subs'].split(', ')
    return parts['name'], parts['weight'], parts['subs']


def build_tables(input_list):
    children = dict()
    parents = dict()
    weights = dict()
    for line in input_list:
        name, weight, subs = parse_input(line)
        children[name] = subs
        weights[name] = int(weight)
        if subs:
            for child in subs:
                parents[child] = name

    return children, parents, weights


def get_root(parents_tree):
    random_child, random_parent = parents_tree.popitem()
    while True:
        try:
            random_parent = parents_tree[random_parent]
        except KeyError:
            break
    return random_parent


def find_bad_weight(children_tree, weights_table):
    def _get_weight(name):
        """To be called recursively to compute cumulative weight of node and its children."""
        # Optimization (e.g., memoization) doesn't seem necessary.
        children = children_tree[name]
        childweight = sum(_get_weight(child) for child in children) if children else 0
        return weights_table[name] + childweight

    cumulative_weight = {name: _get_weight(name) for name in children_tree}

    weight_adjust = list()
    for name, children in children_tree.items():
        if children:
            childweights = [cumulative_weight[child] for child in children]

            # All the weights should match, but if they don't there should be only one different weight
            if len(set(childweights)) >= 2:
                weights_counter = Counter(childweights)
                good_weight, bad_weight = (x[0] for x in weights_counter.most_common(2))
                bad_node = children[childweights.index(bad_weight)]
                weight_adjust.append(dict(name=bad_node,
                                          old_weight=cumulative_weight[bad_node],
                                          new_weight=weights_table[bad_node] + good_weight - bad_weight))

    # The lightest of the "bad nodes" here must be the culprit and the heavier ones are it's ancestors
    weight_adjust = sorted(weight_adjust, key=lambda d: d['old_weight'])
    return weight_adjust[0]['new_weight']


def get_answers(input_list):
    children_tree, parents_tree, weights_table = build_tables(input_list)
    root = get_root(parents_tree)
    new_weight = find_bad_weight(children_tree, weights_table)

    return root, new_weight


print("Root Node: {}, New Weight: {}".format(*get_answers(test_input)))
print("Root Node: {}, New Weight: {}".format(*get_answers(puzzle_input)))
