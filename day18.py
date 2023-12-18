import re

import scrib
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer

directions = { 'D': (1,0), 'L': (0,-1), 'U': (-1,0), 'R': (0,1)}
dir_list = ['D', 'L', 'U', 'R']
def add_point(p1,p2):
    return (p1[0]+p2[0],p1[1]+p2[1])


def shoelace(v):
    sum = 0
    for index in range(len(v)):
        index_plus = (index + 1) % len(v)


        sum += v[index][1]*v[index_plus][0] - v[index_plus][1]*v[index][0]

        # print("(y_{}+y_{}) * (x_{}-x_{})".format(index, index_plus, index, index_plus))
        # sum += (v[index][0] + v[index_plus][0])*(v[index][1]-v[index_plus][1])
    return(sum/2)


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    g = {}
    pos = (0,0)
    visited = set()
    open_list = set()
    closed_list = set()

    v = (0,0)
    vertices = [v]
    for l in lines:
        d, s, c = l.split()
        c = c[1:-1]
        s = int(s)
        # print(d,c,s)

        for i in range(s):
            pos = add_point(pos,directions[d])

            inside = add_point(pos,directions[dir_list[(dir_list.index(d) + 1) % len(dir_list)]])
            open_list.add(inside)
            closed_list.add(pos)
            visited.add((pos, c))


        v = add_point(v,tuple([s*x for x in directions[d]]))
        vertices.append(v)

    # for t in range(len(vertices)):
    #     test = vertices[:t]
    #     print("Shoelace {}={}".format(test, shoelace(test)))
    p1 = int(shoelace(vertices) + len(visited)/2 + 1)

    v = (0,0)
    vertices = [v]
    perimiter = 0

    for l in lines:
        d, s, c = l.split()
        c = c[1:-1]

        s = int(c[1:6], 16)
        d = dir_list[(int(c[6:]) + 3) % len(dir_list)]
        perimiter += s
        v = add_point(v,tuple([s*x for x in directions[d]]))
        print("{} {}".format(d,s))
        vertices.append(v)

    p2 = int(shoelace(vertices) + perimiter/2 + 1)

    # while len(open_list) > 0:
    #     m = open_list.pop()
    #     # print("Open",m)
    #     # print("Open size {}".format(len(open_list)))
    #     closed_list.add(m)
    #     if m not in [v[0] for v in visited]:
    #         for n in [add_point(m,a) for a in directions.values()]:
    #             # print("Neighbor",n)
    #             if n not in closed_list and n not in open_list and n not in [v[0] for v in visited]:
    #                 open_list.add(n)
    #         visited.add((m, None))
    #
    # # print_grid(visited)
    #
    # p1 = len(set([v[0] for v in visited]))
    return p1, p2


def print_grid(visited):
    max_r = max([v[0][0] for v in visited])
    max_c = max([v[0][1] for v in visited])
    min_r = min([v[0][0] for v in visited])
    min_c = min([v[0][1] for v in visited])

    max_r = min(max_r,50)
    max_c = min(max_c,50)
    for r in range(min_r,max_r + 1):
        for c in range(min_c,max_c + 1):
            if (r, c) in [v[0] for v in visited]:
                print("#", end="")
            else:
                print(" ", end="")
        print()


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("Elapsed time {}".format(timer()-start))
    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
