import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer

def n(grid,p):
    n_list = []
    for r, c in [(-1,0), (1,0), (0,1), (0,-1)]:
            n_list.append((p[0]+r,p[1]+c))
    return n_list


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    # grid = s.parsegrid(lines)

    g = []
    # max_r = len(lines)
    # max_c = len(lines[0])

    # g = [k for k in grid if grid[k] == "#"]
    # ex_r = [r for r in range(max_r) if all([scrib.get(grid,r,c)=='.' for c in range(max_c+1)])]
    # ex_c = [c for c in range(max_c) if all([scrib.get(grid,r,c)=='.' for r in range(max_r+1)])]

    grid = {(r,c): item for r, line in enumerate(lines) for c,item in enumerate(line)}
    g = [(r, c) for r, line in enumerate(lines) for c,item in enumerate(line) if item == "#"]

    print(n(grid,g[0]))
    print(g[0],g[1])
    print(s.a_star_algorithm(grid, g[0], g[1], n))

    ex_r = [r for r, item in enumerate(lines) if all(i == "." for i in item)]
    ex_c = [c for c, item in enumerate(zip(*lines)) if all(i == "." for i in item)]

    d_p1 = {}
    d_p2 = {}
    for k, g1 in enumerate(g):
        for j, g2 in enumerate(g[:k+1]):
            exp_r = (sum([1 for r in ex_r if r in range(*sorted([g1[0],g2[0]]))]))
            exp_c = (sum([1 for c in ex_c if c in range(*sorted([g1[1],g2[1]]))]))

            d_p2[(g1,g2)] = s.distance(g1,g2) + exp_r*999999 + exp_c*999999
            d_p1[(g1,g2)] = s.distance(g1,g2) + exp_r + exp_c

    return sum(d_p1.values()), sum(d_p2.values())


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    p1, p2 = solve(input_file)
    assert(p1==9370588)
    assert(p2==746207878188)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("elapsed time {}".format(timer()-start))
    # print("day 8 part 1: {}".format(part1("./data/day10_test.txt")))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
