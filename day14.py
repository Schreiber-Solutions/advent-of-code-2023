import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    g = lines
    p1, p2 = 0, 0

    r = lines

    cache = []
    possible = []
    iteration = 0

    while len(possible) < 100:
        if p1 == 0:
            r1 = tilt(r, 0)
            p1 = sum([(len(r1) - i) * len([e for e in r1[i] if e == "O"]) for i in range(len(r1))])

        r = spin(r)

        w = sum([(len(r) - i) * len([e for e in r[i] if e == "O"]) for i in range(len(r))])
        if w in cache:
            possible.append(iteration)
        cache.append(w)
        iteration += 1

    start, pattern = s.find_repeating_sequence(cache)
    if start < 0:
        print("Unable to find pattern")
        p2 = -1
    else:
        p2 = pattern[(1000000000 - 1 - start) % len(pattern)]
    return p1, p2


def map_key(m):
    return "".join(m)

map_cache = {}
def spin(map):
    k = map_key(map)
    if k in map_cache.keys():
        return map_cache[k]
    r = map

    for i in range(4):
        r = tilt(r,i)

    map_cache[k] = r
    return r


def print_display(r):
    for l in r:
        print("".join(l))
    print()


def tilt(lines,position):
    # 0 north, 1 west, 2 south, 3 east
    if position % 2 == 0:
        lines = list(zip(*lines))

    if position > 1:
        lines = [s.reverse_list(l) for l in lines]

    result = []
    for r in lines:
        chunks = str(r).split("#")
        result.append("#".join(["".join(['O' for a in chunk if a == 'O']) + "".join(['.' for a in chunk if a == '.']) for chunk in chunks]))
    lines = result

    if position > 1:
        lines = [s.reverse_list(l) for l in lines]

    if position % 2 == 0:
        lines = list(zip(*lines))

    return lines


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("elapsed {}".format(timer()-start))
    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
