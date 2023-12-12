import re

import scrib
import scrib as s
import os
from collections import namedtuple
import itertools, operator

def fu(s,c):
    for index, source in enumerate(s):
        if source == "?":
            a = s[:index] + "." + s[index + 1:]
            if all([item != '?' for item in a]):
                # print("{} -> {}".format(s,a))

                r = 0
                occ = [len(g) for g in re.split(r"(\.+)", a) if all(item != '.' for item in g) and len(g) > 0]
                if (occ == c):
                    # print(occ, c)
                    r += 1

                a = s[:index] + "#" + s[index + 1:]
                # print("{} -> {}".format(s,a))

                occ = [len(g) for g in re.split(r"(\.+)", a) if all(item != '.' for item in g) and len(g) > 0]
                if (occ == c):
                    # print(occ, c)
                    r += 1

                return r
            else:
                current = [len(g) for g in re.split(r"(\.+)",s[:index]) if all(item != '.' for item in g) and len(g) > 0]
                # print(current,c[:len(current)])
                if current == c[:len(current)]:
                    r1 = fu(s[:index] + "." + s[index + 1:],c)
                else:
                    r1 = 0

                # print(current[:-1],c[:len(current)-1],current[-1],c[len(current)-1])
                if len(current) > len(c):
                    r2 = 0
                elif len(current) < 1 or (current[:-1] == c[:len(current)-1] and current[-1] <= c[len(current)-1]):
                    r2 = fu(s[:index] + "#" + s[index + 1:],c)
                else:
                    r2 = 0

                return r1 + r2

    if [len(g) for g in re.split(r"(\.+)",s) if all(item != '.' for item in g) and len(g) > 0] == c:
        return 1
    else:
        return 0

def way(c,s):
    dots = len(s)-sum(c)-len(c)+1
    guy = [[r] for r in range(0,dots)]
    print(guy)
    print(len(c))

    for i in range(len(c)):
        for g in guy:
            g.append(c[i])

        if i == len(c):
            start = 0
        else:
            start = 1

        new_guy = []
        for a in range(start,dots):
            for g in guy:
                tmp = g.copy()
                tmp.append(a)
                new_guy.append(tmp)

        guy = new_guy
        guy = [g for g in guy if sum(g) <= len(s)]
        print(i,len(guy))
    guy = [g for g in guy if sum(g)==len(s)]
    return(len(guy))

def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    r1, r2 = 0, 0


    for which, l in enumerate(lines):
        print("doing {}".format(which))
        s, c = l.split()
        c = [int(n) for n in c.split(",")]

        retval1 = fu(s,c)
        r1 += retval1
        print("part 1: {}".format(retval1))

        s_p2 = "?".join([s,s,s,s,s])
        c_p2 = [*c, *c, *c, *c, *c]
        # print(s_p2,c_p2)

        retval2 = 0
        if max(c) == 3 and s_p2.find("?###?") >= 0:
            print("old:" + s_p2)
            s_p2 = s_p2.replace("?###?", ".###.")
            print("new:" + s_p2)

        if c[0] == 1 and s_p2[:3] == "?#?":
            s_p2 = ".#." + s_p2[3:]

        print("{} has {} ?".format(s_p2, sum([1 for item in s_p2 if item == "?"])))
        mid = int(len(s_p2)/2)
        if s_p2.find(".") < 0:
            # retval2=way(c_p2,s_p2)
            retval2 = 0 # fu(s_p2, c_p2)
        else:
            while s_p2[mid] != ".":
                mid = mid - 1

            for index in range(len(c_p2)):
                # print("trying {} with {} and {} with {}".format(s_p2[:mid],c_p2[:index],s_p2[mid:],c_p2[index:]))
                a,b = fu(s_p2[:mid],c_p2[:index]),fu(s_p2[mid:],c_p2[index:])
                # print("got {} and {}".format(a,b))
                retval2 += a*b

        print("part 2: {}".format(retval2))
        r2 += retval2
        # 864204545186 too low
    return r1, r2


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
