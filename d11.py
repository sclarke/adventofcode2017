from collections import Counter

with open('d11_input.txt') as f:
    puzzle_input = f.read().strip().split(',')


def simplify_path(path):

    # looks like the order matters here; need to cancel out the 0-dist pairs first
    # would need collections.OrderedDict if this wasn't Python 3.6
    reduce_table = {
        ('n', 's'): '',
        ('nw', 'se'): '',
        ('ne', 'sw'): '',
        ('n', 'se'): 'ne',
        ('ne', 's'): 'se',
        ('se', 'sw'): 's',
        ('s', 'nw'): 'sw',
        ('sw', 'n'): 'nw',
        ('nw', 'ne'): 'n',
    }

    step_counts = Counter(path)
    for direction_pair, direction_replacement in reduce_table.items():
        replace_count = min(step_counts[direction] for direction in direction_pair)
        for direction in direction_pair:
            step_counts[direction] -= replace_count
        if direction_replacement:
            step_counts[direction_replacement] += replace_count

    return step_counts


def calculate_distance(path):
    pos = Counter()
    furthest = 0
    for step in path:
        pos.update([step])
        pos = simplify_path(pos)
        furthest = max(sum(pos.values()), furthest)
    return furthest


print(sum(simplify_path('ne,ne,ne'.split(',')).values()))
print(sum(simplify_path('ne,ne,sw,sw'.split(',')).values()))
print(sum(simplify_path('ne,ne,s,s'.split(',')).values()))
print(sum(simplify_path('ne,ne,ne'.split(',')).values()))
print(sum(simplify_path('se,sw,se,sw,sw'.split(',')).values()))
print(sum(simplify_path(puzzle_input).values()))

print(calculate_distance(puzzle_input))
