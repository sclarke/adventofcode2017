
from collections import Counter

test_input = ["aa bb cc dd ee",
              "aa bb cc dd aa",
              "aa bb cc dd aaa",
              ]

with open('d04_input.txt') as f:
    puzzle_input = f.readlines()

def check_line(line):
    count = Counter(line.split())

    return True if max(count.values()) == 1 else False

print(sum(check_line(phrase) for phrase in test_input))
print(sum(check_line(phrase) for phrase in puzzle_input))
