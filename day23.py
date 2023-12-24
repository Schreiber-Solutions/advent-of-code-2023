import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer
from collections import deque

def get_grid(grid, r, c):
    if r >= 0 and r< len(grid) and c >= 0 and c < len(grid[0]):
        return grid[r][c]
    else:
        return "#"

dirs = [(1,0), (0,1), (-1,0), (0,-1)]
hills = ['v', '>', '^', '<']

def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    start_node = [(0,c) for c, col in enumerate(lines[0]) if col == "."][0]
    end_node = [(len(lines)-1,c) for c, col in enumerate(lines[len(lines)-1]) if col == "."][0]
    print(end_node)
    open_list = { start_node }
    visited = { start_node: 0 }
    path = {start_node: [] }

    while open_list:
        m = open_list.pop()
        # print(path)
        mr, mc = m
        # print(open_list)
        for (dr, dc) in [d for index, d in enumerate(dirs) if hills[index] == get_grid(lines, *m) or get_grid(lines, *m) == '.']:
            if get_grid(lines, mr+dr, mc+dc) != "#":
                # print("{} neighbor {}".format(m,(mr+dr,mc+dc)))
                if (mr+dr,mc+dc) not in path[m]:
                    if (mr+dr,mc+dc) not in visited:
                        visited[(mr+dr,mc+dc)] = visited[m] + 1
                        path[(mr+dr,mc+dc)] = [(mr+dr,mc+dc), *path[m]]
                        open_list.add((mr+dr,mc+dc))

                    elif visited[(mr+dr,mc+dc)] < visited[m] + 1:
                        visited[(mr + dr, mc + dc)] = visited[m] + 1
                        path[(mr+dr,mc+dc)] = [(mr+dr,mc+dc), *path[m]]
                        open_list.add((mr+dr,mc+dc))

    p = path[end_node]
    p.reverse()
    print(len(p))
    p1 = visited[end_node]

    # reversed
    start_node = [(0,c) for c, col in enumerate(lines[0]) if col == "."][0]
    end_node = [(len(lines)-1,c) for c, col in enumerate(lines[len(lines)-1]) if col == "."][0]


    junctions = [start_node]
    for r, row in enumerate(lines):
        for c, item in enumerate(row):
            if item != '#' and sum([1 for (dr,dc) in dirs if get_grid(lines, r+dr, c+dc) != '#']) > 2:
                junctions.append((r,c))
    junctions.append(end_node)
    print("Junctions {}".format(junctions))
    paths = { start_node: () }
    open_list = { (start_node, ) }
    closed_list = set()
    while open_list:
        # print(open_list)
        m = open_list.pop()
        for j1 in [j for j in junctions if j != m[0] and j not in [closed_item[0] for closed_item in closed_list]]:
            result = find_short_path(j1, m[0], lines)
            # direct path without intermediate junctions
            if result and sum([1 for p in result if p in junctions]) == 2:
                paths[(m[0],j1)] = result
                paths[(j1,m[0])] = result
                open_list.add((j1, *m))
                print("{}->{}: {}".format(m[0],j1,result))
        closed_list.add(m)

    print("result {}".format([c for c in closed_list if c[0]==end_node]))
    max_len = 0
    for result in [c for c in closed_list if c[0] == end_node]:
        print([paths[k] for k in [(p1,result[index+1]) for index, p1 in enumerate(result[:-1])]])
        if sum([len(paths[k]) for k in [(p1,result[index+1]) for index, p1 in enumerate(result[:-1])]]) > max_len:
            max_len = sum([len(paths[k]) for k in [(p1,result[index+1]) for index, p1 in enumerate(result[:-1])]])

    p2 = max_len
    # closed_list = find_long_path(end_node, lines, start_node)
    # print("there are {} paths".format(len([c for c in closed_list if c[0] == end_node])))
    # max_len = max([len(c) for c in closed_list if c[0] == end_node])
    # p2 = [c for c in closed_list if c[0] == end_node and len(c) == max_len][0]
    # print("biggest {}".format(max_len))
    #
    # print_path(lines, p2)
    # p2 = len(p2)-1
    return p1, p2

    # 1902 too low
    # 5606 too low
    # not 5607
    # not 5638
    # 5690 at 10:33 not until 10:43
    # 5946 not right
    # 6170 not right


def find_short_path(start_node, end_node, lines):
    open_list = [(start_node,)]
    closed_list = set()
    max_len = 1000000
    p2 = []
    while open_list:
        # open_list.sort(reverse=True, key=by_len)
        open_list.sort(key=lambda elem: by_len(elem) + s.distance(elem[0], end_node))
        m = open_list.pop(0)

        mr, mc = m[0]
        # print(len(open_list))

        all_m = [m, *[p for p in open_list if p[0] == m]]
        long_m = max([len(p) for p in all_m])
        long_m = [p for p in all_m if len(p) == long_m][0]

        for m in all_m:
            if m in open_list:
                open_list.remove(m)

            for (dr, dc) in dirs:
                if get_grid(lines, mr + dr, mc + dc) != "#":
                    # print("{} neighbor {}".format(m[0],(mr+dr,mc+dc)))
                    if (mr + dr, mc + dc) == end_node:
                        if len(m) < max_len:
                            closed_list.add(((mr + dr, mc + dc), *m))
                            max_len = len(m)
                            # print_path(lines, m)
                        # print("Found end node with length {} ({} - {} open, {} closed)".format(len(m), max_len,
                        #                                                                        len(open_list),
                        #                                                                        len(closed_list)))

                    else:
                        if len(m)+1 < max_len:
                            if all([(mr + dr, mc + dc) not in p for p in all_m]) and m == long_m:
                                open_list.append(((mr + dr, mc + dc), *m))
                            elif (mr + dr, mc + dc) not in m:
                                open_list.append(((mr + dr, mc + dc), *m))

            # for o in open_list:
            #     print(o)
    min_len = min([len(c) for c in closed_list if c[0] == end_node])
    retval = [c for c in closed_list if c[0] == end_node and len(c) == min_len]

    if len(retval) > 0:
        return retval[0]
    else:
        return None

def find_long_path(end_node, lines, start_node):
    open_list = [(start_node,)]
    closed_list = set()
    max_len = 0
    p2 = []
    while open_list:
        # open_list.sort(reverse=True, key=by_len)
        open_list.sort(reverse=True, key=lambda elem: by_len(elem) + s.distance(elem[0], end_node))
        m = open_list.pop(0)

        mr, mc = m[0]
        # print(len(open_list))

        all_m = [m, *[p for p in open_list if p[0] == m]]
        long_m = max([len(p) for p in all_m])
        long_m = [p for p in all_m if len(p) == long_m][0]

        for m in all_m:
            if m in open_list:
                open_list.remove(m)

            for (dr, dc) in dirs:
                if get_grid(lines, mr + dr, mc + dc) != "#":
                    # print("{} neighbor {}".format(m[0],(mr+dr,mc+dc)))
                    if (mr + dr, mc + dc) == end_node:
                        if len(m) > max_len:
                            closed_list.add(((mr + dr, mc + dc), *m))
                            max_len = len(m)
                            # print_path(lines, m)
                        print("Found end node with length {} ({} - {} open, {} closed)".format(len(m), max_len,
                                                                                               len(open_list),
                                                                                               len(closed_list)))

                        p2_max_len = max([len(c) for c in closed_list if c[0] == end_node])
                        p2 = [c for c in closed_list if c[0] == end_node and len(c) == p2_max_len][0]
                    else:
                        if all([(mr + dr, mc + dc) not in p for p in all_m]) and m == long_m:
                            open_list.append(((mr + dr, mc + dc), *m))
                        elif (mr + dr, mc + dc) not in m:
                            open_list.append(((mr + dr, mc + dc), *m))

            # for o in open_list:
            #     print(o)
    return closed_list


def print_path(lines, p2):
    for r in range(len(lines)):
        for c in range(len(lines[0])):
            if (r, c) in p2:
                print("O", end="")
            else:
                print(get_grid(lines, r, c), end="")

        print()


def by_len(elem):
    return len(elem)


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]
    start = timer()
    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("elapsed {}".format(timer()-start))
    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
