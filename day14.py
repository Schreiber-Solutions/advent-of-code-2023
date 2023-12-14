import re
import scrib as s
import os
from collections import namedtuple


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    g = lines
    p1, p2 = 0, 0

    r = lines

    cache = []
    possible = []

    for i in range(200):
        r = tilt_north_south(r, False)
        if p1 == 0:
            p1 = sum([(len(r) - i) * len([e for e in r[i] if e == "O"]) for i in range(len(r))])

        r = tilt_east_west(r, False)

        r = tilt_north_south(r, True)

        r = tilt_east_west(r, True)
        # print_display(r)
        w = sum([(len(r) - i) * len([e for e in r[i] if e == "O"]) for i in range(len(r))])
        if w in cache:
            possible.append(i)
        cache.append(w)

    possible = [possible[i] for i in range(len(possible)-1) if possible[i+1]==possible[i]+1]

    start = possible[0]
    possible = [cache[p] for p in possible]
    pattern = []
    for k in range(1,len(possible)+1):
        if possible[:k]*2 == possible[:2*k]:
            pattern = possible[:k]
            break

    p2 = pattern[(1000000000 - 1 - start) % len(pattern)]

    # p2 = [69, 69, 65, 64, 65, 63, 68][999971990 % 7]
    # p2 =  [90212,
    #          90217,
    #          90213,
    #          90200,
    #          90188,
    #          90177,
    #          90176,
    #          90182,
    #          90198,
    #          90211,
    #          90218,
    #          90212,
    #          90201,
    #          90187,
    #          90178,
    #          90175,
    #          90183,
    #          90197][(1000000000 - 1 - 363) % 18]

    return p1, p2



def print_display(r):
    for l in r:
        print("".join(l))
    print()


def tilt_east_west(lines, is_east):
    rows = lines
    if is_east:
        rows = [s.reverse_list(l) for l in rows]

    new_rows = []
    for r in rows:
        chunks = str(r).split("#")
        new_chunks = []
        for chunk in chunks:
            n = "".join(['O' for a in chunk if a == 'O']) + "".join(['.' for a in chunk if a == '.'])
            new_chunks.append(n)
        new_rows.append("#".join(new_chunks))

    if is_east:
        new_rows = [s.reverse_list(l) for l in new_rows]

    return new_rows


def tilt_north_south(lines, is_south):
    cols = list(zip(*lines))
    if is_south:
        cols = [s.reverse_list(l) for l in cols]

    new_cols = []
    for c in cols:
        chunks = str(c).split('#')
        new_chunks = []
        for chunk in chunks:
            n = "".join(['O' for a in chunk if a == 'O']) + "".join(['.' for a in chunk if a == '.'])
            new_chunks.append(n)
        # print("#".join(new_chunks))
        new_cols.append("#".join(new_chunks))

    if is_south:
        new_cols = [s.reverse_list(l) for l in new_cols]

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
