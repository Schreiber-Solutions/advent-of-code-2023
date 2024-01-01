import re
import scrib as s
import os
from timeit import default_timer as timer
import math
import sys

def find_shortest_path(map, a, b):
    open_list = { a }
    closed_list = set()
    parent = { a: a }
    distance = { a: 0 }

    min_len = math.inf
    while open_list:
        m = open_list.pop()

        for n in map[m]:
            if n == b:
                p = m
                path = [n, m]
                # print("reconstructing with a {}, b {}, n {}, m {}, parent {}".format(a, b, n, m, parent))
                while parent[p] != a:
                    path.append(parent[p])
                    p = parent[p]
                path.append(a)
                path.reverse()
                return path
            elif n not in closed_list:
                if n in distance and distance[n] > distance[m] + 1:
                    parent[n] = m
                    distance[n] = distance[m] + 1
                    open_list.add(n)
                else:
                    parent[n] = m
                    distance[n] = distance[m] + 1
                    open_list.add(n)

        closed_list.add(m)

    return None


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    G = {}
    all = []
    for l in lines:
        left, right = l.split(": ")
        right = right.split()

        for r in right:
            all.append((left,r))
            # all.append((r,left))

            if left in G.keys():
                G[left].add(r)
            else:
                G[left] = {r}

            if r in G.keys():
                G[r].add(left)
            else:
                G[r] = {left}

    all = list(set(all))

    # ('xkz','mvv')
    # ('pnz','tmt')
    # ('hxr','gbc')

    start=timer()
    all_list = list([a[0] for a in all])

    max_len = 0
    p = [ 0 ]
    a = all_list[0]
    # max_pair = ('cxf', 'thr')
    max_pair = ()

    if len(max_pair) < 2:
        for i in range(0,len(all_list),len(all_list)//10):
            b = all_list[i]
            for j in range(i+1,len(all_list),(len(all_list)-i-1)//10+1):
                a = all_list[j]
                p = find_shortest_path(G, a, b)
                if len(p) > max_len:
                    max_len = len(p)
                    max_pair = (b,a)
            if max_len > 30:
                break

    max_len = 0
    paths = []

    one_end = { max_pair[0] }
    other_end = { max_pair[1]}

    intersection = []

    steps = 1
    while not intersection:
        for i in range(steps):
            n_one_end = one_end.copy()
            for p in one_end:
                n_one_end.update(G[p])
            one_end = n_one_end

        for i in range(steps):
            n_other_end = other_end.copy()
            for p in other_end:
                n_other_end.update(G[p])
            other_end = n_other_end

        steps += 1

        intersection.extend([o for o in one_end if o in other_end])
        one_end = one_end - other_end

    unit = 5000
    cap = unit
    p1 = None
    while not p1:
        new_top_3 = []
        smaller_map = G
        for i in range(3):
            top_5 = top_5_segments(smaller_map, one_end, other_end, cap)
            top = top_5[0]
            # print(top)
            new_top_3.append(top)
            smaller_map = remove_map(G,*top)

        print("Top 3 is ", new_top_3)

        start = timer()
        my_groups = set()

        exclude = new_top_3
        revised_map = {k: [l for l in i if (k, l) not in exclude and (l, k) not in exclude] for
                       k, i in G.items()}
        result = find_shortest_path(revised_map, *max_pair)
        if result is not None:
            print("No solution found")
            cap += unit

        else:
            for item in new_top_3:
                for z in item:
                    res = find_all(revised_map, z, list(new_top_3))
                    res = tuple(sorted(list(res)))
                    my_groups.add(res)

                if len(my_groups) == 2:
                    acc = 1
                    for g in my_groups:
                        acc = acc * len(g)
                    p1 = acc
                    # print(acc)

    return p1, p2


def top_5_segments(G, one_end, other_end, cap):
    segment_distribution = {}
    for i, a in enumerate(one_end):
        for b in other_end:
            p = find_shortest_path(G, a, b)
            for point_index, point in enumerate(p[:-1]):
                if (point, p[point_index + 1]) in segment_distribution:
                    segment_distribution[(point, p[point_index + 1])] += 1
                elif (p[point_index + 1], point) in segment_distribution:
                    segment_distribution[(p[point_index + 1], point)] += 1
                else:
                    segment_distribution[point, p[point_index + 1]] = 1
        segment_use = sorted(list(segment_distribution.values()), reverse=True)[:5]

        current_tally = [s for s in
                         sorted([(s, d) for s, d in segment_distribution.items() if d in segment_use],
                                key=lambda z: z[1],
                                reverse=True)][0][1]
        if current_tally > cap:
            break
    segment_use = sorted(list(segment_distribution.values()), reverse=True)[:5]
    # print("Top 5: ", [s for s in sorted([(s,d) for s,d in segment_distribution.items() if d in segment_use],key=lambda z : z[1], reverse=True)][:8], "elapsed ", timer()-start)
    top_5 = [s[0] for s in
             sorted([(s, d) for s, d in segment_distribution.items() if d in segment_use], key=lambda z: z[1],
                    reverse=True)][:5]
    return top_5


def remove_map(map, a, b):
    new_map = map.copy()

    if b in new_map[a]:
        new_map[a].remove(b)
    if a in new_map[b]:
        new_map[b].remove(a)

    return new_map


def find_all(map, a, exclude):
    open_list = { a }
    result = set()
    while open_list:
        m = open_list.pop()

        if m in [k for k, d in map.items() if (k, d) not in exclude and (d, k) not in exclude]:
            for n in [d for d in map[m] if (m, d) not in exclude and (d, m) not in exclude]:
                if n not in result:
                    open_list.add(n)
        result.add(m)
    return tuple(result)


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    start = timer()
    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))
    print("Elapsed: ", timer()-start)
