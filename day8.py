import re
import scrib
import os
from collections import namedtuple
from math import lcm


def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    map = {}
    for index in range(2, len(input_lines)):
        l = input_lines[index]
        a, b, c = re.findall(r"\w{3}", l)
        map[a] = [b, c]

    instructions = input_lines[0]

    next_node = [k for k in map.keys() if k[-1] == 'A']
    which = {}
    while len(which) < len(next_node):
        for i in instructions:
            if i == "L":
                next_node = [map[k][0] for k in next_node]
            else:
                next_node = [map[k][1] for k in next_node]

            total = total + 1
            if len([n for n in next_node if n[-1] == "Z"]) == 1:
                matches = [n for n in next_node if n[-1] == "Z"]
                which[next_node.index(matches[0])] = total

            if len(next_node) == (len([n for n in next_node if n[-1] == "Z"])):
                return total

    return lcm(*list(which.values()))


def get_prime_factors(n):
    i = 2
    prime_factors = []
    while i * i <= n:
        if n % i == 0:
            prime_factors.append(i)
            n //= i
        else:
            i += 1

    if n > 1:
        prime_factors.append(n)

    return prime_factors


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    map = {}
    for index in range(2, len(input_lines)):
        l = input_lines[index]
        a, b, c = re.findall(r"\w{3}", l)
        map[a] = [b, c]
        # map[l.split(" = ")[0]] = ["".join([l for l in raw if l not in ['(',')']]) for raw in l.split(" = ")[1].split(", ")]

    instructions = input_lines[0]
    instruction_numbers = [0 if c == 'L' else 1 for c in instructions]
    next_node = "AAA"

    while True:
        for i in instruction_numbers:
            next_node = map[next_node][i]
            total = total + 1

            if next_node == "ZZZ":
                return total


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d) - 3]

    input_file = "./data/" + d + "_input.txt"
    print("{} part 1: {}".format(d, part1(input_file)))
    assert (part1(input_file) == 22199)
    print("{} part 2: {}".format(d, part2(input_file)))
    assert (part2(input_file) == part2(input_file))
