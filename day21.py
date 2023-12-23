import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer

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
def finder(grid, start, length):
    open = { (start) }
    visited = {start: 0}
    points = set()

    if (start, length) in cache.keys():
        return cache[(start,length)][0]

    # options = [k[1] for k in cache.keys() if k[0] == start and k[1] < length and k[1] % 2 == length % 2]
    # if options:
    #     print("Found options {},{} for {}".format(start, length, options))
    #     points, visited = cache[(start,max(options))]
    #     print("Visited for {},{} len {} is {}".format(start, max(options), len(visited), visited))
    #     open = {v for v in visited if visited[v] == max(visited.values())}
    #     print("Starting with points {}".format(points))

    if length == 0:
        return points

    while open:
        m = open.pop()
        mr, mc = m
        for dr, dc in dirs:
            if mr+dr < 0 or mr+dr >= len(grid) or mc+dc < 0 or mc+dc >= len(grid[0]):
                tmp = ((mr+dr) % len(grid), (mc+dc) % len(grid[0]))
                tmp_length = length - visited[(mr,mc)] - 1
                if tmp_length > 0:
                    # print("{} -> {} with length {}".format((mr+dr, mc+dc), tmp, tmp_length))
                    offset_r = mr+dr-tmp[0]
                    offset_c = mc+dc-tmp[1]
                    if grid_get(grid, *tmp) != "#":
                        beyond = [(offset_r+p[0],offset_c+p[1]) for p in finder(grid, tmp, tmp_length)]
                        # print(beyond)
                        points.update(beyond)

                    if (visited[(mr, mc)] + 1) % 2 == length % 2:
                        points.add((mr + dr, mc + dc))

            elif grid_get(grid, mr + dr, mc + dc) != "#" and visited[(mr,mc)] + 1 <= length:
                # if int((visited[(mr,mc)] + 1) / 100) ==(visited[(mr,mc)] + 1) / 100:
                #     print((visited[(mr,mc)] + 1))

                if (mr+dr, mc+dc) not in visited:
                    open.add((mr+dr, mc+dc))
                    visited[(mr+dr, mc+dc)] = visited[(mr,mc)] + 1
                else:
                    if visited[(mr+dr, mc+dc)] > visited[(mr,mc)] + 1:
                        visited[(mr + dr, mc + dc)] = visited[(mr, mc)] + 1
                        open.add((mr + dr, mc + dc))

                if (visited[(mr, mc)] + 1) % 2 == length % 2:
                    points.add((mr+dr, mc + dc))

    # print(points)
    cache[(start,length)] = [points, visited]

    return points

def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0
    start_node = [(r,c) for r, row in enumerate(lines) for c, col in enumerate(lines[r]) if lines[r][c] == "S"][0]

    start = timer()
    print(6, len(finder(lines, start_node, 6)), timer()-start)
    print(10, len(finder(lines, start_node, 10)), timer()-start)
    print(50, len(finder(lines, start_node, 50)), timer()-start)
    print(100, len(finder(lines, start_node, 100)), timer()-start)
    print(500, len(finder(lines, start_node, 500)), timer()-start)

    return 0,0
    # p1 = len(finder(lines, start_node, 64))
    # p2 = finder(lines, start_node, 100)


    for i in range(101, 200, 2):
        tmp = int(i/len(lines))+1
        print("{}:".format(i))
        tmp_points = finder(lines, start_node, i)
        for r_offset in range(-tmp,tmp+1):
            for c_offset in range(-tmp,tmp+1):
                all_points_rc = [(r+r_offset*len(lines),c+c_offset*len(lines[0])) for r, row in enumerate(lines) for c, col in enumerate(lines[r]) if c != "#"]
                print("{:>8}\t\t".format(len([p for p in all_points_rc if p  in tmp_points])), end="")
            print()
        print()


    p2 = len(p2)
    #  3113198559 (too low)
    # min_r = min([r for r,c in p2])
    # max_r = max([r for r,c in p2])
    # min_c = min([c for r,c in p2])
    # max_c = max([c for r,c in p2])
    #
    # for r in range(min_r, max_r+1):
    #     for c in range(min_c, max_c+1):
    #         if (r,c) == start_node:
    #             print("S", end="")
    #         elif (r,c) in p2:
    #             print("O", end="")
    #         else:
    #             print(lines[r % len(lines)][c % len(lines[0])], end="")
    #     print()

    return p1, p2


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("Elapsed {}".format(timer()-start))
    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
