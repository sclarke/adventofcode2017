

with open('d09_input.txt') as f:
    puzzle_input = f.read()


def handle_garbage(stream):
    count = 0
    while True:
        gc = next(stream)
        if gc == "!":
            next(stream)  # advance iter, ignore next char
        elif gc == ">":
            return count
        else:
            count += 1


def parse_stream(stream, nest_level=0):
    score = 0
    garbage_count = 0
    while True:

        try:
            c = next(stream)
        except StopIteration:
            return score, garbage_count

        if c == "{":
            substr_score, substr_garbage_count = parse_stream(stream, nest_level + 1)
            score += substr_score
            garbage_count += substr_garbage_count
        elif c == "<":
            garbage_count += handle_garbage(stream)
        elif c == "}":
            return nest_level + score, garbage_count
        else:
            pass  # not an interesting character?


print(parse_stream(iter("{{},{}}")))
print(parse_stream(iter("{{{},{},{{}}}}")))
print(parse_stream(iter("{<a>,<a>,<a>,<a>}")))
print(parse_stream(iter("{{<ab>},{<ab>},{<ab>},{<ab>}}")))
print(parse_stream(iter("{{<!!>},{<!!>},{<!!>},{<!!>}}")))
print(parse_stream(iter("{{<a!>},{<a!>},{<a!>},{<ab>}}")))

print(parse_stream(iter(puzzle_input)))
