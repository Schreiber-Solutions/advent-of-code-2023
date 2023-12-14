import re
import scrib as s
import os
from collections import namedtuple


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    g = lines
    p1, p2 = 0, 0

    r = tilt_north_south(lines, True)
    for l in r:
        print("".join(l))

    p1 = sum([(len(r)-i)*len([e for e in r[i] if e == "O"]) for i in range(len(r))])
    len(r)
    return p1, p2


def tilt_north_south(lines, is_south):
    cols = list(zip(*lines))
    if is_south:
        lines = [s.reverse_list(l) for l in lines]

    new_cols = []
    for c in cols:
        chunks = str(c).split('#')
        new_chunks = []
        for chunk in chunks:
            n = "".join(['O' for a in chunk if a == 'O']) + "".join(['.' for a in chunk if a == '.'])
            new_chunks.append(n)
        # print("#".join(new_chunks))
        new_cols.append("#".join(new_chunks))
    r = list(zip(*new_cols))
    return r


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
