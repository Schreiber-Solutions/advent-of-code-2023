import re
import scrib
import os
from collections import namedtuple


def part2(input):
    with open(input) as f:
        lines = f.read().splitlines()

    t = 0

    return t

moves = {'|': ['|', 'L','J','7','F'],
         '-': ['-', 'L','J','7','F'],
         'L': ['|','-','J','7'],
         'J': ['|','-','L','7','F'],
         '7': ['|','-','J','L','F'],
         'F': ['|','-','J','7','L'],
         'S': ['|','-','J','7','L', 'F'],
         '.': []}
map = {'|': [(-1,0),(1,0)],
        '-': [(0,1),(0,-1)],
        'L': [(-1,0),(0,1)],
        'J': [(-1,0),(0,-1)],
        '7': [(1,0),(0,-1)],
        'F': [(1,0),(0,1)],
         'S': [(1,0),(0,1),(-1,0),(0,-1)],
       '.': []}
def n(grid,r,c):
    n = []
    m = scrib.get(grid,r,c)

    for x1 in [-1,0,1]:
        for x2 in [-1,0,1]:
            if x1 != x2 and x1 != -1*x2:
                e = grid.get((r+x1,c+x2))
                if e in map.keys() and (-1*x1,-1*x2) in map[e] and (m == 'S' or (x1,x2) in map[m]):
                    n.append((r+x1,c+x2))
                # else:
                #     if m != 'S':
                #         print((-x1,-x2),m, e, map[m],map[e])

    return n

def p(grid,path):
    for r in range(max([n[0] for n in grid.keys()])+1):
        for c in range(max([n[1] for n in grid.keys()])+1):
            if (r,c) in path:
                print(scrib.get(grid,r,c),end="")
            else:
                print(".",end="")
        print()

def part1(input):
    with open(input) as f:
        lines = f.read().splitlines()

    grid = scrib.parsegrid(lines)

    start=(0,0)
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if scrib.get(grid,r,c) == "S":
                start = (r,c)

    path = [start]

    e = n(grid,start[0],start[1])[0]
    while e not in path:
        path.append(e)
        # print(len(path))
        if e == start or len([a for a in n(grid,*e) if a not in path]) == 0:
            p(grid,path)
            return(len(path)/2)
        else:
            if len(n(grid,*e)) > 2:
                print("{} neighbors {}".format(e,n(grid,*e)))

            e = [a for a in n(grid,*e) if a not in path][0]

    t = 0
    return t


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    print("{} part 1: {}".format(d,part1(input_file)))
    print("{} part 2: {}".format(d,part2(input_file)))
    # print("day 8 part 1: {}".format(part1("./data/day10_test.txt")))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))

    # GRID WORK
    # grid = scrib.parsegrid(lines)
    # scrib.get(grid,0,0)
