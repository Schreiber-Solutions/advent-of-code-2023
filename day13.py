import re
import scrib as s
import os
from collections import namedtuple

def vary(m):
    retval = []

    for r,l in enumerate(m):
        for c,item in enumerate(l):
            m_p = m.copy()
            if item=='#':
                t = "."
            else:
                t = "#"
            # print(c, m_p[r])
            m_p[r] = m_p[r][:c] + t + m_p[r][c+1:]
            retval.append(m_p)
    return retval

def check_v(m):
    columns = list(zip(*m))

    max_c = len(columns)
    for c, col in enumerate(columns):

        if (c < len(columns) - 1):
            if columns[c] == columns[c + 1]:
                many = min(abs(max_c - c - 2), c)

                if all(columns[c - i] == columns[c + 1 + i] for i in range(0, many + 1)):
                    return c
    return -1

def check_h(m):
    max_r = len(m)
    for r in range(max_r - 1):
        if m[r] == m[r + 1]:
            many = min(abs(max_r - r - 2), r)

            if all(m[r - i] == m[r + 1 + i] for i in range(0, many + 1)):
                # print("v-line",r)
                return r
    return -1

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

    p1 = {}

    for m in g:
        print("map:",m_count)
        max_r = len(m)
        for r in range(max_r-1):
            if m[r] == m[r+1]: ## check more rows
                many = min(abs(max_r-r-2),r)

                # for i in range(0,many+1):
                #     print(r,i,r-i,r+1+i,(m[r-i],m[r+1+i]),max_r)

                if all(m[r-i] == m[r+1+i] for i in range(0,many+1)):
                    print(r,[m[r-i] == m[r+1+i] for i in range(0,many+1)])
                    h.append(r+1)
                    p1[m_count] = "h"+str(r)

        m_count = m_count + 1
    print(h)

    v = []
    m_count = 0
    for m in g:
        columns = list(zip(*m))
        print("map:",m_count)
        max_c = len(columns)
        for c, col in enumerate(columns):

            if (c<len(columns)-1):
                if columns[c] == columns[c+1]:
                    many = min(abs(max_c-c-2), c)

                    if all(columns[c-i]== columns[c+1+i] for i in range(0,many+1)):
                        v.append(c+1)
                        p1[m_count] = "v"+str(c)
        m_count = m_count + 1

    print(len(p1))
    # print(p1)

    h2 = []
    v2 = []
    p2 = {}

    print("begin part 2")
    m_count = 0
    for m_original in g:
        print("map {}".format(m_count))
        for m in vary(m_original):
            # print("map {} variant".format(m))
            r = check_h(m)
            if r >= 0 and "h"+str(r) != p1[m_count]:
                print("Found h {} (was {})".format(r,p1[m_count]))
                h2.append(r + 1)
                p2[m_count] = "h" + str(r)
                break

            c = check_v(m)
            if c >= 0 and "v" + str(c) != p1[m_count]:
                print("Found v {}".format(c))
                v2.append(c + 1)
                p2[m_count] = "v" + str(c)
                break

        m_count = m_count + 1

    p1 = sum(v)
    p1 = p1 + sum([n*100 for n in h])


    print(len(p2),p2)
    print(h2, v2)

    return p1, sum(v2) + sum([n*100 for n in h2])
    # part 2 10770 is too low
    # part 2 32334 too high

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
