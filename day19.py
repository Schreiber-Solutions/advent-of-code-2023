import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    b = s.lines_to_blocks(lines)
    workflows = {}
    for w in b[0]:
        n, c = re.findall(r"(\w+){(.+)}", w)[0]
        c = [m.split(":") for m in c.split(",")]

        workflows[n] = [a for a in c if len(a) > 1]
        workflows[n].append(["True", c[-1][0]])
        # print(n,c)
    p1, p2 = 0, 0

    for part in b[1]:
        coords = re.findall(r"(\w+)=(\d+)", part)
        coords = {a[0]: int(a[1]) for a in coords}

        w = workflows["in"]

        b_done = False
        while not b_done:
            for c in w: # condition
                result = c[0]
                if len(c) > 1:
                    next = c[1]
                    for v in coords:
                        result = result.replace(v,str(coords[v]))

                else:
                    next = c[0]
                    result = "True"

                if eval(result):

                    if next == "A":
                        p1 += sum(coords.values())
                        b_done = True
                    elif next == "R":
                        b_done = True
                    else:
                        w = workflows[next]
                    break

    A_total = calculate_degrees("A", workflows)
    total_degrees = A_total
    p2 = total_degrees
    # Build the tree from in down to either A or R
    # for all leaves that end in A, recreate all the conditions - that's the range of possible 0-4000
    return p1, p2


def calculate_degrees(start, workflows):
    total_degrees = 0
    for a in find_conditions(workflows, start):
        degrees_of_freedom = []
        for c in ['x', 'm', 'a', 's']:
            min_c = 1
            max_c = 4000
            for crit in [x for x in a if x[0] == c]:
                dx = 0 if crit.find("=")>0 else 1
                if crit.find(">") > 0:
                    if s.find_int(crit) + dx > min_c:
                        min_c = s.find_int(crit) + dx
                if crit.find("<") > 0:
                    if s.find_int(crit) - dx < max_c:
                        max_c = s.find_int(crit) - dx

            if max_c > min_c:
                degrees_of_freedom.append(max_c - min_c + 1)
                # print("{} between {} and {} with {} has {} degrees".format(c, min_c, max_c, [x for x in a if x[0] == c],
                #                                                            max_c - min_c + 1))
            else:
                degrees_of_freedom.append(0)

        total_degrees += (degrees_of_freedom[0] * degrees_of_freedom[1] * degrees_of_freedom[2] * degrees_of_freedom[3])
    return total_degrees


def find_conditions(workflows, target):
    # print(target, [a for a in workflows if target in [t[1] for t in workflows[a]]])
    ret_val = []
    for w in [a for a in workflows if target in [t[1] for t in workflows[a]]]:
        for index, c in enumerate(workflows[w]): # condition
            if c[1] == target:
                prev_cond = [workflows[w][a][0] for a in range(0,index)]
                np_cond = []
                for p in prev_cond:
                    if p.find(">")>0:
                        np_cond.append(p.replace(">","<="))
                    if p.find("<")>0:
                        np_cond.append(p.replace("<", ">="))
                prev_cond = np_cond

                if c[0] != "True":
                        prev_cond.append(c[0])

                # ret_val.append(prev_cond)

                gen = find_conditions(workflows, w)
                if len(gen) == 0:
                    ret_val.append (prev_cond)
                else:
                    for g in gen:
                        ret_val.append([*g, *prev_cond])
    return ret_val

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
