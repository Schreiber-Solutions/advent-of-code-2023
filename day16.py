import re
import sys

import scrib as s
import os
from collections import namedtuple

def print_map(map, e, beams):
    for r, l in enumerate(map):
        for c, item in enumerate(l):
            if (r,c) in [b[0] for b in beams]:
                print("O", end="")
            elif (r,c) in e:
                print("#", end="")
            else:
                print(map[r][c], end = "")
        print()

def add_point(p1,p2):
    return (p1[0]+p2[0],p1[1]+p2[1])

def solve(input):
    sys.setrecursionlimit(5000)
    with open(input) as f:
        lines = f.read().splitlines()

    map = lines
    start = (0,0)
    start_dir = (0,1)

    e = r_solve(map, start, start_dir)
    print("Part 1 {}".format(len(e)))
    print_map(map,e,[])

    es = [-1]
    global my_cache

    for r in range(len(map)):
        print("varying row {} max e {}".format(r, max(es)))
        start = (r,0)
        my_cache = {}
        es.append(len(r_solve(map,start,(0,1))))
        assert(es[1]==len(e))

        start = (r,len(map[0])-1)
        my_cache = {}
        es.append(len(r_solve(map, start, (0, -1))))

    for c in range(len(map[0])):
        my_cache = {}
        print("varying col {} max e {}".format(c, max(es)))
        start = (0,c)
        es.append(len(r_solve(map,start,(1,0))))

        my_cache = {}
        start = (len(map)-1,c)
        es.append(len(r_solve(map,start,(-1,0))))

    p1, p2 = len(e), max(es)

    return p1, p2

my_cache = {}
def r_solve(map, pos, dir, path=[]):
    if (*pos, *dir) in my_cache.keys():
        k = (*pos, *dir)
        return my_cache[k]

    if not(0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])):
        return []

    g = map[pos[0]][pos[1]]

    new_beams = []

    if g == "|" and dir in [(0, 1), (0, -1)]:
        # make two
        new_beams.append([pos, (1, 0)])
        new_beams.append([pos, (-1, 0)])

    elif g == "-" and dir in [(1, 0), (-1, 0)]:
        # make two

        new_beams.append([pos, (0, 1)])
        new_beams.append([pos, (0, -1)])
    elif g == "/" and dir in [(0, 1), (0, -1)]:
        new_beams.append([pos, (dir[1] * -1, 0)])

    elif g == "/" and dir in [(1, 0), (-1, 0)]:
        new_beams.append([pos, (0, dir[0] * -1)])

    # \
    elif g == "\\" and dir in [(1, 0), (-1, 0)]:
        new_beams.append([pos, (0, dir[0])])

    elif g == "\\" and dir in [(0, 1), (0, -1)]:
        new_beams.append([pos, (dir[1], 0)])

    else:
        new_beams.append([pos, dir])

    illuminated = []
    for b in new_beams:
        if [add_point(b[0],b[1]), b[1]] not in path:
            # if b[0] in [p[0] for p in path]:
            #     print("Trying beam {}".format(b))
            #     print("Path {}".format([p for p in path if p[0] == b[0]]))
            illuminated.extend([pos, *r_solve(map, add_point(b[0],b[1]), b[1], [[pos, dir], *path])])
        else:
            illuminated.extend([pos])

    ret_val =list(set(illuminated))

    if (*pos, *dir) not in my_cache.keys():
        k = (*pos, *dir)
        my_cache[k] = ret_val


    return ret_val


def solve2(map, start, start_dir):
    last_e = [-1]
    e = [start]
    beams = [[start, start_dir]]
    cycles = 0
    path = []

    # while not all(b in path for b in beams):
    while not all([len(e) == l_e for i, l_e in enumerate(last_e)]):
        # while cycles < 50:
        path.extend(beams)
        last_e.append(len(e))
        last_e = last_e[len(last_e) - 5:]
        # print([l_e for i, l_e in enumerate(last_e[len(last_e)-5:])])
        cycles = cycles + 1
        # print("beams {}".format(len(beams)))
        new_beams = []

        for index, b in enumerate(beams):
            pos = b[0]
            dir = b[1]
            if 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0]):
                g = map[pos[0]][pos[1]]
                # print(g, pos, dir, g == "\\" and dir in [(0,1),(0,-1)])
                if g == "|" and dir in [(0, 1), (0, -1)]:
                    # make two
                    new_beams.append([pos, (1, 0)])
                    new_beams.append([pos, (-1, 0)])

                elif g == "-" and dir in [(1, 0), (-1, 0)]:
                    # make two

                    new_beams.append([pos, (0, 1)])
                    new_beams.append([pos, (0, -1)])
                elif g == "/" and dir in [(0, 1), (0, -1)]:
                    new_beams.append([pos, (dir[1] * -1, 0)])

                elif g == "/" and dir in [(1, 0), (-1, 0)]:
                    new_beams.append([pos, (0, dir[0] * -1)])

                # \
                elif g == "\\" and dir in [(1, 0), (-1, 0)]:
                    new_beams.append([pos, (0, dir[0])])

                elif g == "\\" and dir in [(0, 1), (0, -1)]:
                    new_beams.append([pos, (dir[1], 0)])

                else:
                    new_beams.append([pos, dir])

        beams = new_beams

        new_beams = []
        for index, b in enumerate(beams):
            pos = b[0]
            dir = b[1]

            pos = add_point(pos, dir)
            if pos[0] >= 0 and pos[0] < len(map) and pos[1] >= 0 and pos[1] < len(map[0]):
                new_beams.append([pos, dir])

        new_poses = [item[0] for item in new_beams]
        new_poses = list(set(new_poses))
        e.extend(new_poses)
        e = list(set(e))

        beams = new_beams
    return e



if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
