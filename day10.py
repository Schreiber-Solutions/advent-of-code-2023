import re
import scrib
import os
from collections import namedtuple

print_map = {'|':u"\u2503", '-':u"\u2501", 'L':u"\u2517", 'J':u"\u251b", 'F':u"\u250f", '7':u"\u2513", 'S':'S'}

map = {'|': [(-1,0),(1,0)],
        '-': [(0,1),(0,-1)],
        'L': [(-1,0),(0,1)],
        'J': [(-1,0),(0,-1)],
        '7': [(1,0),(0,-1)],
        'F': [(1,0),(0,1)],
         'S': [(1,0),(0,1),(-1,0),(0,-1)],
       '.': []}

included = ['|', 'S', '7','F']


def n(grid,r,c):
    n = []
    m = scrib.get(grid,r,c)

    for x1 in [-1,0,1]:
        for x2 in [-1,0,1]:
            if x1 != x2 and x1 != -1*x2:
                e = grid.get((r+x1,c+x2))
                if e in map.keys() and (-1*x1,-1*x2) in map[e] and (m == 'S' or (x1,x2) in map[m]):
                    n.append((r+x1,c+x2))

    return n


def count_included(grid,path):
    new_i_count = 0

    for r in range(max([n[0] for n in grid.keys()])+1):
        i_parity = 0
        for c in range(max([n[1] for n in grid.keys()])+1):
            me = scrib.get(grid,r,c)
            if (r,c) in path and me in included:
                i_parity = (i_parity + 1) % 2
            elif (r,c) not in path:
                new_i_count += i_parity

    return new_i_count


def p(grid,path,inside):
    i_count = 0
    new_i_count = 0

    for r in range(max([n[0] for n in grid.keys()])+1):
        i_parity = 0
        for c in range(max([n[1] for n in grid.keys()])+1):
            if (r,c) in path:
                print(print_map[scrib.get(grid,r,c)],end="")
            elif (r,c) in inside:
                i_count += 1
                print("I", end="")
            else:
                print(i_parity, end="")
                # print(" ",end="")

            me = scrib.get(grid,r,c)
            if (r,c) in path and me in included:
                i_parity = (i_parity + 1) % 2
            elif (r,c) not in path:
                new_i_count += i_parity

        print()
    print("included count {} (new count {})".format(i_count,new_i_count))


check = {(0,-1): (-1,0), (1,0): (0,-1), (0,1): (1,0), (-1,0): (0,1)}


def add(x1,x2):
    return (x1[0]+x2[0],x1[1]+x2[1])


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
            # complete path

            # inside = find_inside_tiles(grid, path)
            # p(grid,path,inside)
            # print(len(inside)) # 1024 is too high, 392 too low

            return(int(len(path)/2),count_included(grid,path))
        else:
            if len(n(grid,*e)) > 2:
                print("{} neighbors {}".format(e,n(grid,*e)))

            e = [a for a in n(grid,*e) if a not in path][0]

    t = 0
    return t


def find_inside_tiles(grid, path):
    inside = []
    for p_i in range(len(path) - 1):
        step = (path[p_i + 1][0] - path[p_i][0], path[p_i + 1][1] - path[p_i][1])
        for i in range(2): # from and to tiles
            target = (path[p_i + i][0] + check[step][0], path[p_i + i][1] + check[step][1])
            if target not in path:
                grid[target] = "I"
                inside.append(target)

    made_changes = True
    while made_changes:
        new_inside = inside.copy()
        made_changes = False
        for i in inside:
            for s in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                if add(i, s) not in path and add(i, s) not in inside and add(i, s) not in new_inside:
                    new_inside.append(add(i, s))
                    grid[add(i, s)] = "I"
                    made_changes = True

        inside = list(set(new_inside))

    return inside


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    p1,p2=part1(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
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
