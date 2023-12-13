import re
import scrib as s
import os
from collections import namedtuple


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    g = []
    m = []
    for l in lines:
        r = 0
        if l != "":
            m.append(l)
            r = r + 1
        else:
            g.append(m)
            r = 0
            m = []
    g.append(m)

    h = []
    m_count = 0

    for m in g:
        print("map:",m_count)
        m_count = m_count + 1

        max_r = len(m)
        for r in range(max_r-1):
            if m[r] == m[r+1]: ## check more rows
                many = min(abs(max_r-r-2),r)

                for i in range(0,many+1):
                    print(r,i,r-i,r+1+i,(m[r-i],m[r+1+i]),max_r)

                if all(m[r-i] == m[r+1+i] for i in range(0,many+1)):
                    print(r,[m[r-i] == m[r+1+i] for i in range(0,many+1)])
                    h.append(r+1)
    print(h)

    v = []
    m_count = 0
    for m in g:
        columns = list(zip(*m))
        print("map:",m_count)
        m_count = m_count + 1
        max_c = len(columns)
        for c, col in enumerate(columns):

            if (c<len(columns)-1):
                if columns[c] == columns[c+1]:
                    many = min(abs(max_c-c-2), c)

                    if all(columns[c-i]== columns[c+1+i] for i in range(0,many+1)):
                        print(c,[columns[c-i]== columns[c+1+i] for i in range(0,many+1)])
                        v.append(c+1)

    print(sum(v),sum(h))
    p1 = sum(v)
    p1 = p1 + sum([n*100 for n in h])

#32927  - too low

    return p1, p2


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
