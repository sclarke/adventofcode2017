from string import ascii_uppercase

test_input = """
     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+ 
""".strip('\n').splitlines()

with open('d19_input.txt') as f:
    puzzle_input = f.readlines()


def get_init_column(line):
    for i, char in enumerate(line):
        if char == "|":
            return i


def follow_line(r, c, maze, updown):
    maze_slice = [line[c] for line in maze] if updown else maze[r]
    long, lat = (r, c) if updown else (c, r)  # longitudinal and lateral direction depends on updown vs leftright mode
    line_char = '|' if updown else '-'
    line_char += "+" + ascii_uppercase

    if long + 1 in range(len(maze_slice)) and maze_slice[long + 1] in line_char:
        direction = 1
    elif long - 1 in range(len(maze_slice)) and maze_slice[long - 1] in line_char:
        direction = -1
    else:
        raise SyntaxError

    steps = 0
    signs = []
    finished = False
    while True:
        long += direction
        if long not in range(len(maze_slice)):
            break
        elif maze_slice[long] == " ":
            if maze_slice[long - direction] == "+":
                break
            else:
                finished = True
                break
        elif maze_slice[long] in ascii_uppercase:
            signs.append(maze_slice[long])
        steps += 1

    new_row, new_col = (long - direction, lat) if updown else (lat, long - direction)
    return new_row, new_col, finished, signs, steps


def follow_path(path):
    row, col = 0, get_init_column(path[0])
    sign_posts = []
    total_steps = 0
    vertical_mode = True
    finished = False

    while not finished:
        row, col, finished, new_sign_posts, steps = follow_line(row, col, path, vertical_mode)
        sign_posts += new_sign_posts
        total_steps += steps
        vertical_mode ^= True

    return ''.join(sign_posts), total_steps + 1


print(follow_path(test_input))
print(follow_path(puzzle_input))
