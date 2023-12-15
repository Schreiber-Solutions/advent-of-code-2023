import re
import scrib as s
import os
from collections import namedtuple


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    lines = lines[0].split(",")

    v = 0

    for l in lines:
        v = v + my_hash(l)

    box = [[] for b in range(256)]

    cache = {}
    for l in lines:
        label = re.search(r"(\w+)", l)
        label = label[0]
        op = re.search(r"[-|=]", l)
        op = op[0]
        # print(op)
        h = my_hash(str(label))

        if op == "=":
            n = s.find_int(l)
            if str(label) in box[h]:
                cache[str(label)] = n
            else:
                box[h].append(label)
                cache[str(label)] = n
        else:
            if label in box[h]:
                box[h].remove(label)

    p2 = 0
    for i, b in enumerate(box):
        for k, lens in enumerate(b):
            p2 = p2 + (i + 1) * (k + 1) * cache[lens]

    return v, p2


def my_hash(l,acc=0):
    if l:
        return my_hash(l[1:],(acc+ord(l[0]))*17 % 256)
    else:
        return acc


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d) - 3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    assert(p1==508498)
    assert(p2==279116)
    print("{} part 1: {}".format(d, p1))
    print("{} part 2: {}".format(d, p2))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
