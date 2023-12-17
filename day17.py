import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer

def add_p(p1, p2):
    return (p1[0]+p2[0],p1[1]+p2[1])

def neighbors_v2(g, p):
    # p is a tuple with at most three sets of paired coordinates - the last being my current point
    most_blocks = 10
    most_dir = most_blocks * 2 + 2
    min_blocks = 4
    min_dir = min_blocks * 2 + 2

    ret = []
    if len(p) < 2:
        raise "Error"
    r, c = p[0], p[1]
    path = p[:most_dir-2]

    for i in [(1,0), (0,1), (-1,0), (0, -1)]:
        new_p = add_p((r,c), i)

        # print(path)
        # print(path[len(path)-2:])
        # print([add_p((r,c),i)[0] == p[0] for p in path[len(path)-2:]])
        if len(p) > 2 and new_p == (p[2],p[3]):
            continue
        elif len(p) == most_dir and all([new_p[0] == item for index, item in enumerate(p) if index % 2 == 0]):
            continue
        elif len(p) == most_dir and all([new_p[1] == item for index, item in enumerate(p) if index % 2 == 1]):
            continue
        elif new_p[0] >= 0 and new_p[0] < len(g) and new_p[1] >= 0 and new_p[1] < len(g[0]):
            if len(p) > 1 and all([new_p[0] == item for index, item in enumerate(p[:4]) if index % 2 == 0]):
                ret.append((*new_p, *path))
            elif len(p) > 1 and all([new_p[1] == item for index, item in enumerate(p[:4]) if index % 2 == 1]):
                ret.append((*new_p, *path))
            elif len([item for index, item in enumerate(p[:min_dir]) if index % 2 == 0 and p[0]==item])==min_blocks+1:
                ret.append((*new_p, *path))
            elif len([item for index, item in enumerate(p[:min_dir]) if index % 2 == 1 and p[1]==item])==min_blocks+1:
                ret.append((*new_p, *path))

    return ret

def validate_p2(p):
    most_blocks = 10
    most_dir = most_blocks * 2 + 2
    min_blocks = 4
    min_dir = min_blocks * 2 + 2

    min_h = all([item == p[0] for index, item in enumerate(p[:min_dir]) if index % 2 == 0])
    min_v = all([item == p[1] for index, item in enumerate(p[:min_dir]) if index % 2 == 1])
    return min_h or min_v

def validate_p1(p):
    return True

def neighbors(g, p):
    # p is a tuple with at most three sets of paired coordinates - the last being my current point
    most_blocks = 3
    most_dir = most_blocks * 2 + 2
    min_blocks = 0

    ret = []
    if len(p) < 2:
        raise "Error"
    r, c = p[0], p[1]
    path = p[:most_dir-2]

    for i in [(1,0), (0,1), (-1,0), (0, -1)]:
        new_p = add_p((r,c), i)

        # print(path)
        # print(path[len(path)-2:])
        # print([add_p((r,c),i)[0] == p[0] for p in path[len(path)-2:]])
        if len(p) > 2 and new_p == (p[2],p[3]):
            continue
        elif len(p) == most_dir and all([new_p[0] == item for index, item in enumerate(p) if index % 2 == 0]):
            continue
        elif len(p) == most_dir and all([new_p[1] == item for index, item in enumerate(p) if index % 2 == 1]):
            continue
        elif new_p[0] >= 0 and new_p[0] < len(g) and new_p[1] >= 0 and new_p[1] < len(g[0]):
            ret.append((*new_p, *path))

    return ret

def a_star_algorithm(grid, start_node, stop_node, get_neighbors, validate):
    # def get_neighbors(grid,p):


    # open_list is a list of nodes which have been visited, but who's neighbors
    # haven't all been inspected, starts off with the start node
    # closed_list is a list of nodes which have been visited
    # and who's neighbors have been inspected
    open_list = set([start_node])
    closed_list = set([])

    # g contains current distances from start_node to all other nodes
    # the default value (if it's not found in the map) is +infinity
    g = {start_node: 0}

    # parents contains an adjacency map of all nodes
    parents = {start_node: start_node}

    while len(open_list) > 0:
        n = None

        # find a node with the lowest value of f() - evaluation function
        for v in open_list:
            if n is None or g[v] < g[n]:
                n = v

        # print("n",n)
        # print(len(open_list))
        # print("Open List", open_list)
        # print("Closed List", closed_list)
        # print("Current g", g)

        if n is None:
            print('Path does not exist!')
            return None

        # if the current node is the stop_node
        # then we begin reconstructin the path from it to the start_node
        if (n[0],n[1]) == stop_node and validate(n):
            reconst_path = []

            while parents[n] != n:
                reconst_path.append(n)
                n = parents[n]

            reconst_path.append(start_node)

            reconst_path.reverse()

            return reconst_path

        # for all neighbors of the current node do
        for m in get_neighbors(grid,n):
            # print("neighbor",m)
            # if the current node isn't in both open_list and closed_list
            # add it to open_list and note n as it's parent
            if m not in open_list and m not in closed_list:
                # print("adding {} to open list with parent {}".format(m,n))
                open_list.add(m)
                parents[m] = n
                g[m] = g[n] + int(grid[m[0]][m[1]])

            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update parent data and g data
            # and if the node was in the closed_list, move it to open_list
            else:
                # print("neighbor {} has {} where {} has {}".format(m, g[m], n, g[n]))
                weight = int(grid[m[0]][m[1]])
                if g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n

                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

        # remove n from the open_list, and add it to closed_list
        # because all of his neighbors were inspected
        open_list.remove(n)
        closed_list.add(n)

    # print('Path does not exist!')
    return None


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    grid = lines
    start_n = (0,0)
    stop_n = (len(grid)-1,len(grid[0])-1)

    # p = ()
    # for i in range(0,11):
    #     p = (0, i, *p)
    #     print(p,neighbors_v2(grid, p))
    #
    # return 0,0
    # print(neighbors(grid, (0,2), [(0,0), (0,1)]))
    res = a_star_algorithm(grid, start_n, stop_n, neighbors, validate_p1)

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if (r,c) in [(item[0],item[1]) for item in res[1:]]:
                print("X", end="")
            else:
                print(col, end="")
        print()
    print()
    p1 = sum([int(grid[item[0]][item[1]]) for item in res[1:] ])

    res = a_star_algorithm(grid, start_n, stop_n, neighbors_v2, validate_p2)

    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if (r,c) in [(item[0],item[1]) for item in res[1:]]:
                print("X", end="")
            else:
                print(col, end="")
        print()
    p2 = sum([int(grid[item[0]][item[1]]) for item in res[1:] ])

    return p1, p2
#931 too high

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
