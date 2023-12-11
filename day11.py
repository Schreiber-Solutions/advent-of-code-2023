import re
import scrib
import os
from collections import namedtuple


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    grid = scrib.parsegrid(lines)

    g = []
    max_r = len(lines)
    max_c = len(lines[0])

    g = [k for k in grid if grid[k] == "#"]

    ex_r = [r for r in range(max_r) if all([scrib.get(grid,r,c)=='.' for c in range(max_c+1)])]
    ex_c = [c for c in range(max_c) if all([scrib.get(grid,r,c)=='.' for r in range(max_r+1)])]

    d_p1 = {}
    d_p2 = {}
    for g1 in g:
        for g2 in g:
            if g1 != g2:
                if (g1,g2) not in d_p1.keys() and (g2,g1) not in d_p1.keys():
                    d_p2[(g1,g2)] = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1]) + sum([999999 for r in ex_r if min(g1[0],g2[0]) < r < max(g1[0],g2[0])]) + sum([999999 for c in ex_c if min(g1[1],g2[1]) < c < max(g1[1],g2[1])])
                    d_p1[(g1,g2)] = abs(g1[0]-g2[0]) + abs(g1[1]-g2[1]) + sum([1 for r in ex_r if min(g1[0],g2[0]) < r < max(g1[0],g2[0])]) + sum([1 for c in ex_c if min(g1[1],g2[1]) < c < max(g1[1],g2[1])])

    return sum(d_p1.values()), sum(d_p2.values())


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    # print("day 8 part 1: {}".format(part1("./data/day10_test.txt")))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
