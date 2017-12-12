
test_input = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5""".strip().splitlines()

with open('d12_input.txt') as f:
    puzzle_input = f.readlines()


def build_groups(inp):
    return dict(parse_line(line) for line in inp)


def parse_line(line):
    """return the index and direct links described by a string representing a pipe"""
    k, v = line.strip().split(' <-> ')
    return k, v.split(', ')


def get_all_links(pipes, root_node="0"):
    """given a dict of links, walk the tree to find all possible endpoints from a given startpoint"""
    new_nodes = links = {root_node}
    while True:
        new_links = set()
        for node in new_nodes:
            new_links |= set(pipes[node])

        if new_links.issubset(links):
            break
        else:
            links |= new_links
            new_nodes = new_links

    return links


def get_all_groups(pipes):
    """given a dict of links, remove a family of nodes until all the families are gone"""
    groups = list()
    while pipes:
        random_node = next(iter(pipes))
        links = get_all_links(pipes, root_node=random_node)
        groups.append(links)
        for link in links:
            del pipes[link]
    return groups


print(len(get_all_links(build_groups(test_input))))
print(len(get_all_links(build_groups(puzzle_input))))

print(len(get_all_groups(build_groups(test_input))))
print(len(get_all_groups(build_groups(puzzle_input))))
