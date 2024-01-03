import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer
import pandas as pd
import matplotlib.pyplot as pt
import numpy as np


dirs = [(1,0), (0,1), (-1,0), (0,-1)]
def grid_get(grid, r, c):
    if r >= 0 and r < len(grid) and c >= 0 and c < len(grid[0]):
        if grid[r][c] != 'S':
            return grid[r][c]
        elif grid[r][c] == 'S':
            return "."
        else:
            return "#"
    else:
        return "#"

cache = {}


def finder(grid, start, length, use_cache=True):
    open = { start }
    visited = {start: 0}
    points = set()

    if length == 0:
        return points

    while open:
        m = open.pop()
        mr, mc = m


        for dr, dc in dirs:
            nr = (mr + dr) % len(grid)
            nc = (mc + dc) % len(grid[0])
            if grid_get(grid, nr, nc) != "#":

                if visited[(mr, mc)] <= length:
                    if (mr+dr,mc+dc) not in visited:
                        open.add((mr + dr, mc + dc))
                        visited[(mr + dr, mc + dc)] = visited[(mr, mc)]+1
                    elif visited[(mr + dr, mc + dc)] > visited[(mr,mc)] + 1:
                        open.add((mr + dr, mc + dc))
                        visited[(mr + dr, mc + dc)] = visited[(mr, mc)] + 1

                    if (visited[(mr, mc)]+1) % 2 == length % 2:
                        points.add((mr+dr,mc+dc))

    return points


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0
    start_node = [(r,c) for r, row in enumerate(lines) for c, col in enumerate(lines[r]) if lines[r][c] == "S"][0]
    p1 = len(finder(lines, start_node, 64))
    start = timer()
    # print(6, len(finder(lines, start_node, 6)), timer()-start)
    # print(10, len(finder(lines, start_node, 10)), timer()-start)
    # print(100, len(finder(lines, start_node, 100)), timer()-start)
    # print(500, len(finder(lines, start_node, 500)), timer()-start)



    target = 26501365
    assert target % len(lines) == len(lines) // 2
    sequence = []
    # periodicity on the i*grid_len+grid_len//2 as target % grid_len == grid_len // 2
    unit_list = [0, 1, 2]
    for unit in unit_list:

        i = unit*len(lines)+len(lines)//2
        tmp = i//len(lines)+1

        tmp_points = finder(lines, start_node, i)
        # for r_offset in range(-tmp,tmp+1):
        #     for c_offset in range(-tmp,tmp+1):
        #         all_points_rc = [(r+r_offset*len(lines),c+c_offset*len(lines[0])) for r, row in enumerate(lines) for c, col in enumerate(lines[r]) if c != "#"]
        #         print("{:>8}\t\t".format(len([p for p in all_points_rc if p  in tmp_points])), end="")
        #     print()

        sequence.append(len(tmp_points))
        # print(i,len(tmp_points))

    grid_len = len(lines)
    units = target // grid_len

    # tiles = a*units**2 + b*units + c
    # c = sequence[0]
    # sequence[1] = a + b + c
    # b = sequence[1] - a - sequence[0]
    # sequence[2] = 4*a + 2*b + c
    # s[2] = 4*a + 2*s[1] - 2*a - s[0]
    # 2*a = s[2] - 2*s[1] + s[0]
    # a = (sequence[2] - 2*sequence[1] + sequence[0] ) / 2

    c = sequence[0]
    a = (sequence[2] - 2 * sequence[1] + sequence[0]) / 2
    b = sequence[1] - a - sequence[0]


    # df = pd.DataFrame({'x': [*unit_list ], 'y': [*sequence] } )
    # curve fit
    # model = np.poly1d(np.polyfit(df.x, df.y, 2))

    p2 = a*units**2 + b*units + c

    return p1, p2


def print_tiles(lines, p2, start_node):
    min_r = min([r for r, c in p2])
    max_r = max([r for r, c in p2])
    min_c = min([c for r, c in p2])
    max_c = max([c for r, c in p2])
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if (r, c) == start_node:
                print("S", end="")
            elif (r, c) in p2:
                print("O", end="")
            else:
                print(lines[r % len(lines)][c % len(lines[0])], end="")
        print()


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("Elapsed {}".format(timer()-start))
    assert p2 == 620962518745459
    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
