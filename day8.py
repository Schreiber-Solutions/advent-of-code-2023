import re
import scrib
import os
from collections import namedtuple
from math import lcm


def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    graph, instructions = parse(input_lines)

    next_node = [k for k in graph.keys() if k[-1] == 'A']
    which = {}
    while len(which) < len(next_node):
        for i in instructions:
            if i == "L":
                next_node = [graph[k][0] for k in next_node]
            else:
                next_node = [graph[k][1] for k in next_node]

            total = total + 1
            if len([n for n in next_node if n[-1] == "Z"]) == 1:
                matches = [n for n in next_node if n[-1] == "Z"]
                which[next_node.index(matches[0])] = total

            if len(next_node) == (len([n for n in next_node if n[-1] == "Z"])):
                return total

    return lcm(*list(which.values()))


def parse(input_lines):
    graph = {}
    for index in range(2, len(input_lines)):
        l = input_lines[index]
        a, b, c = re.findall(r"\w{3}", l)
        graph[a] = [b, c]
    instructions = input_lines[0]
    return graph, instructions


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    graph, instructions = parse(input_lines)

    instruction_numbers = [0 if c == 'L' else 1 for c in instructions]
    next_node = "AAA"

    while True:
        for i in instruction_numbers:
            next_node = graph[next_node][i]
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
