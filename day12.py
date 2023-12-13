import re
from functools import lru_cache
from typing import List, Tuple
import scrib
import scrib as s
import os
from collections import namedtuple
import itertools, operator

@lru_cache()
def fu(s,c):
    if len(c) == 0:
        return 1 if '#' not in s else 0
    if sum(c) + len(c) - 1 > len(s):
        return 0

    if s[0] == '.':
        return fu(s[1:],c)

    if s[0] == '?':
        r1 = fu(s[1:], c)
    else:
        r1 = 0

    if '.' not in s[:c[0]] and (len(s) <= c[0] or len(s) > c[0] and s[c[0]] != '#'):
        r2 = fu(s[c[0]+1:], c[1:])
    else:
        r2 = 0

    return r1 + r2



def is_valid(s,target):
    if len(s) != len(target):
        return False
    else:
        same = True
        for index, item in enumerate(s):
            # print("compare {} and {}".format(item,target[index]))
            if item != '?' and item != target[index]:
                same = False
        return same


def split_solve(s,c):
    if len(s) == 0:
        return 0

    if len(c) == 1:
        return fu(s,c)
    elif len(c) == 2:
        # retval = fu(s, c)
        # n = 1
        # # print([ [ split_solve(s[:index],c[:n])*split_solve(s[index:],c[n:]),s[:index],c[:n],s[index:],c[n:]] for index in range(len(s)) if s[index-1] != s[index] != "#"])
        combos = [fu(s[:index],c[:1])*fu(s[index:],c[1:]) for index in range(len(s)) if s[index-1] != s[index] != "#"]
        if len(combos) > 0:
            retval = max([fu(s[:index],c[:1])*fu(s[index:],c[1:]) for index in range(len(s)) if s[index-1] != s[index] != "#"])
        else:
            retval = 0
        return retval
    elif len(c)/2 == int(len(c)/2):
        # print("{} {} and {} {}".format(s,c[:int(len(c)/2)],s,c[int(len(c)/2):]))
        n = int(len(c)/2)
        # print([ [ split_solve(s[:index],c[:n])*split_solve(s[index:],c[n:]),s[:index],c[:n],s[index:],c[n:]] for index in range(len(s))])
        # print([ split_solve(s[:index],c[:n])*split_solve(s[index:],c[n:]) for index in range(len(s))])
        retval = max([ split_solve(s[:index],c[:n])*split_solve(s[index:],c[n:]) for index in range(len(s))])
        return retval
    else:
        last_group = "".join(["#"]*c[0]) + "."
        retval = 0

        for index in range(len(s)-sum(c)-len(c)+2):
            target = "".join(['.']*index) + last_group + s[index+c[0]+1:]

            if is_valid(s,target):
                num = split_solve(target[index+len(last_group):],c[1:])
                # print("{} calling split_solve with {} and {} gets {}".format(index,target[index+len(last_group):],c[1:],num))
                retval += split_solve(target[index+len(last_group):],c[1:])
        return retval

def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    r1, r2 = 0, 0


    for which, l in enumerate(lines):
        print("doing {}".format(which))
        s, c = l.split()
        s = tuple(s)
        c = tuple([int(n) for n in c.split(",")])
        print(s,c)
        retval1 = fu(s,c)
        r1 += retval1
        print("part 1: {}".format(retval1))

        # s_p2 = tuple("?".join([s,s,s,s,s]))
        s_p2 = (*s, '?', *s, '?', *s, '?', *s, '?', *s)
        c_p2 = (*c, *c, *c, *c, *c)
        # print(s_p2,c_p2)

        retval2 = 0

        retval2 = fu(s_p2,c_p2)

        print("part 2: {}".format(retval2))
        r2 += retval2
        # 864204545186 too low
    return r1, r2



if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    s = tuple("???.###")
    c = (1, 1, 3)
    print (fu(s, c))
    assert(fu(s,c)==1)

    s = tuple(".??..??...?##.")
    c = (1, 1, 3)
    print (fu(s, c))
    assert(fu(s,c)==4)

    s = tuple("?#?#?#?#?#?#?#?")
    c = (1, 3, 1, 6)
    num = fu(s, c)
    assert num==1, f"expected 1 got {num}"


    s = tuple("????.#...#...")
    c = (4, 1, 1)
    num = fu(s, c)
    assert num==1, f"expected 1 got {num}"

    s = tuple("????.######..#####.")
    c = (1, 6, 5)
    num = fu(s, c)
    assert num==4, f"expected 4 got {num}"

    s = tuple("?###????????")
    c = (3, 2, 1)
    num = fu(s, c)
    assert num==10, f"expected 10 got {num}"

    s = tuple("?###????????")
    c = (3, 2, 1)
    num = fu(s, c)
    assert num==10, f"expected 10 got {num}"

    print("test 2-1")
    s = tuple("????.######..#####.")
    c = (1,6,5)
    s_p2 = (*s, '?', *s, '?', *s, '?', *s, '?', *s)
    c_p2 = (*c, *c, *c, *c, *c)
    num = fu(s_p2,c_p2)
    assert num==2500,f"result is {num} not 2500"

    print("test 2-2")
    s = tuple("?###????????")
    c = (3, 2, 1)
    s_p2 = (*s, '?', *s, '?', *s, '?', *s, '?', *s)
    c_p2 = (*c, *c, *c, *c, *c)
    num = fu(s_p2,c_p2)
    assert num==506250,f"result is {num} not 506250"

    print("start solve")
    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
