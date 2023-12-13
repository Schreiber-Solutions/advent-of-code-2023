import re
import scrib as s
import os
from collections import namedtuple


def vary(m):
    retval = []

    for r, l in enumerate(m):
        for c, item in enumerate(l):
            m_p = m.copy()
            if item == '#':
                t = "."
            else:
                t = "#"
            # print(c, m_p[r])
            m_p[r] = m_p[r][:c] + t + m_p[r][c + 1:]
            retval.append(m_p)
    return retval


def check_v(m, exclude):
    columns = list(zip(*m))

    max_c = len(columns)
    for c, col in enumerate(columns):

        if c < len(columns) - 1:
            many = min(abs(max_c - c - 2), c)
            if c != exclude and all(columns[c - i] == columns[c + 1 + i] for i in range(0, many + 1)):
                return c

    return -1


def check_h(m, exclude):
    max_r = len(m)
    for r in range(max_r - 1):
        many = min(abs(max_r - r - 2), r)

        if r != exclude and all(m[r - i] == m[r + 1 + i] for i in range(0, many + 1)):
            return r

    return -1


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    g = s.lines_to_blocks(lines)

    h = []
    p1 = {}

    for m_count, m in enumerate(g):
        r = check_h(m, -1)
        if r >= 0:
            h.append(r + 1)
            p1[m_count] = "h" + str(r)

    v = []
    for m_count, m in enumerate(g):
        c = check_v(m, -1)
        if c >= 0:
            v.append(c + 1)
            p1[m_count] = "v" + str(c)

    h2 = []
    v2 = []
    p2 = {}

    for m_count, m_original in enumerate(g):
        for m in vary(m_original):
            exclude = s.find_int(p1[m_count]) if p1[m_count][0] == "h" else -1
            r = check_h(m, exclude)
            if r >= 0:
                h2.append(r + 1)
                p2[m_count] = "h" + str(r)
                break

            exclude = s.find_int(p1[m_count]) if p1[m_count][0] == "v" else -1
            c = check_v(m, exclude)
            if c >= 0:
                v2.append(c + 1)
                p2[m_count] = "v" + str(c)
                break

    return sum(v) + sum([n * 100 for n in h]), sum(v2) + sum([n * 100 for n in h2])


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d) - 3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d, p1))
    print("{} part 2: {}".format(d, p2))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
