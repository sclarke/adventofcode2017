
from collections import Counter

test_input = ["aa bb cc dd ee",
              "aa bb cc dd aa",
              "aa bb cc dd aaa",
              ]

with open('d04_input.txt') as f:
    puzzle_input = f.readlines()


def check_line(line):
    count = Counter(line.split())
    return max(count.values()) == 1


print("Test Text", sum(check_line(phrase) for phrase in test_input), '\n')
print("Puzzle Text", sum(check_line(phrase) for phrase in puzzle_input), '\n')


def check_line_2(line):
    count = Counter([''.join(sorted(word)) for word in line.split()])
    return max(count.values()) == 1


print("abcde fghij", check_line_2("abcde fghij"))
print("abcde xyz ecdab", check_line_2("abcde xyz ecdab"))
print("a ab abc abd abf abj", check_line_2("a ab abc abd abf abj"))
print("iiii oiii ooii oooi oooo", check_line_2("iiii oiii ooii oooi oooo"))
print("oiii ioii iioi iiio", check_line_2("oiii ioii iioi iiio"))

print()
print("Puzzle Text", sum(check_line_2(phrase) for phrase in puzzle_input), '\n')
