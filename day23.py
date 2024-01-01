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

    open_list = { start_node }
    visited = { start_node: 0 }
    path = {start_node: [] }

    while open_list:
        m = open_list.pop()
        mr, mc = m

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

    p1 = visited[end_node]

    # reversed
    start_node = [(0,c) for c, col in enumerate(lines[0]) if col == "."][0]
    end_node = [(len(lines)-1,c) for c, col in enumerate(lines[len(lines)-1]) if col == "."][0]

    # open_list = [ (start_node, ) ]
    open_list = deque()
    visited = { (start_node, ): 0 }
    closed_list = set()
    max_len = 0
    open_list.append((start_node, ))

    while open_list:
        # open_list.sort(key=lambda elem: visited[elem] + s.distance(elem[0],end_node), reverse=True)
        m = open_list.pop()

        if m[0] == end_node:
            closed_list.add(m)
            if visited[m] > max_len:
                max_len = visited[m]

        else:
            neighbors = find_neighbors(lines, m[0], end_node)
            for (j1, distance) in neighbors:

                if j1 not in m:
                    open_list.append((j1, *m))
                    visited[(j1, *m)] = visited[m] + distance

    path = [k for k, d in visited.items() if d == max_len]
    if len(path) > 0:
        # print("Longest path", path)
        p2 = max_len
    else:
        p2 = 0

    return p1, p2


cache = {}
def find_neighbors(grid, start_node, end_node):

    if start_node == end_node:
        return []

    if start_node in cache:
        return cache[start_node]

    open_list = [start_node]
    closed_list = set()
    neighbor = set()
    distance = { start_node: 0 }
    # parent = {start_node: start_node }

    while open_list:
        m = open_list.pop()

        mr, mc = m
        if m != start_node and sum([1 for (dr, dc) in dirs if get_grid(grid, mr + dr, mc + dc) != "#"]) > 2:
            neighbor.add((m,distance[m]))
        elif m == end_node:
            neighbor.add((m, distance[m]))
        else:
            for (dr, dc) in dirs:
                if m not in closed_list and get_grid(grid, mr + dr, mc + dc) != "#":
                    open_list.append((mr+dr,mc+dc))
                    distance[(mr+dr,mc+dc)] = distance[m] + 1

            closed_list.add(m)

    if start_node not in cache:
        cache[start_node] = neighbor

    return neighbor


# def find_short_path(start_node, end_node, lines, exclude = []):
#     open_list = [(start_node,)]
#     closed_list = set()
#     max_len = 1000000
#
#     if end_node == start_node:
#         return []
#
#     while open_list:
#         # open_list.sort(reverse=True, key=by_len)
#         open_list.sort(key=lambda elem: by_len(elem) + s.distance(elem[0], end_node))
#         m = open_list.pop(0)
#
#         mr, mc = m[0]
#         # print(len(open_list))
#
#         all_m = [m, *[p for p in open_list if p[0] == m]]
#         long_m = max([len(p) for p in all_m])
#         long_m = [p for p in all_m if len(p) == long_m][0]
#
#         for m in all_m:
#             if m in open_list:
#                 open_list.remove(m)
#
#             for (dr, dc) in dirs:
#                 if (mr+dr, mc+dc) not in exclude:
#                     if get_grid(lines, mr + dr, mc + dc) != "#":
#                         if (mr + dr, mc + dc) == end_node:
#                             if len(m) < max_len:
#                                 closed_list.add(((mr + dr, mc + dc), *m))
#                                 max_len = len(m)
#
#                         else:
#                             if len(m)+1 < max_len:
#                                 if all([(mr + dr, mc + dc) not in p for p in all_m]) and m == long_m:
#                                     open_list.append(((mr + dr, mc + dc), *m))
#                                 elif (mr + dr, mc + dc) not in m:
#                                     open_list.append(((mr + dr, mc + dc), *m))
#
#     retval = [len(c) for c in closed_list if c[0] == end_node]
#     if len(retval) > 0:
#         min_len = min(retval)
#         retval = [c for c in closed_list if c[0] == end_node and len(c) == min_len]
#
#         return s.reverse_list(retval[0])
#     else:
#         return None
#
# def find_long_path(lines, start_node, end_node, exclude):
#     open_list = [(start_node,)]
#     closed_list = set()
#     max_len = 0
#     p2 = []
#     while open_list:
#         # open_list.sort(reverse=True, key=by_len)
#         open_list.sort(reverse=True, key=lambda elem: by_len(elem) + s.distance(elem[0], end_node))
#         m = open_list.pop(0)
#
#         mr, mc = m[0]
#         # print(len(open_list))
#
#         all_m = [m, *[p for p in open_list if p[0] == m]]
#         long_m = max([len(p) for p in all_m])
#         long_m = [p for p in all_m if len(p) == long_m][0]
#
#         for m in all_m:
#             if m in open_list:
#                 open_list.remove(m)
#
#             for (dr, dc) in dirs:
#                 if (mr+dr,mc+dc) not in exclude:
#                     if get_grid(lines, mr + dr, mc + dc) != "#":
#                         # print("{} neighbor {}".format(m[0],(mr+dr,mc+dc)))
#                         if (mr + dr, mc + dc) == end_node:
#                             if len(m) > max_len:
#                                 closed_list.add(((mr + dr, mc + dc), *m))
#                                 max_len = len(m)
#                                 # print_path(lines, m)
#
#                         else:
#                             if all([(mr + dr, mc + dc) not in p for p in all_m]) and m == long_m:
#                                 open_list.append(((mr + dr, mc + dc), *m))
#                             elif (mr + dr, mc + dc) not in m:
#                                 open_list.append(((mr + dr, mc + dc), *m))
#
#             # for o in open_list:
#             #     print(o)
#     result = [len(c) for c in closed_list if c[0] == end_node]
#     if not result:
#         return None
#     p2_max_len = max(result)
#     p2 = [c for c in closed_list if c[0] == end_node and len(c) == p2_max_len][0]
#
#     return p2
#

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
