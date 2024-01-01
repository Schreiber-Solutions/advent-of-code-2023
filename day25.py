import re
import scrib as s
import os
from timeit import default_timer as timer
import math
import sys

def find_paths(map, a, b):
    open_list = { (a,) }
    closed_list = set()

    segment_distribution = {}
    while open_list and len(closed_list) < 400:
        m = open_list.pop()
        # segment_use = sorted(list(segment_distribution.values()), reverse=True)[:5]
        # print("Top 5: ", [s for s in sorted([(s, d) for s, d in segment_distribution.items() if d in segment_use],
        #                                     key=lambda z: z[1], reverse=True)][:5])

        m_label = m[0]
        for n in map[m_label]:
            if n == b:
                # for point_index, point in enumerate(m[:-1]):
                #     if (point, m[point_index + 1]) in segment_distribution:
                #         segment_distribution[(point, m[point_index + 1])] += 1
                #     elif (m[point_index + 1], point) in segment_distribution:
                #         segment_distribution[(m[point_index + 1], point)] += 1
                #     else:
                #         segment_distribution[point, m[point_index + 1]] = 1

                closed_list.add((n, *m))
            elif n not in m:
                open_list.add((n, *m))

    # print(closed_list)
    return closed_list

def find_farthest_v2(map, a):
    open_list = { a }
    closed_list = set()
    parent = { a: a }
    distance = { a: 0 }

    min_len = math.inf
    while open_list:
        m = open_list.pop()

        for n in map[m]:
            if n not in closed_list:
                if n in distance and distance[n] > distance[m] + 1:
                    parent[n] = m
                    distance[n] = distance[m] + 1
                    open_list.add(n)
                else:
                    parent[n] = m
                    distance[n] = distance[m] + 1
                    open_list.add(n)

        closed_list.add(m)

    p = [m for m, d in distance.items() if d == max(distance.values())][0]
    path = [p]
    # print("reconstructing with a {}, b {}, n {}, m {}, parent {}".format(a, b, n, m, parent))
    while parent[p] != a:
        path.append(parent[p])
        p = parent[p]
    path.append(a)
    path.reverse()
    return path


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


def solve2(input):
    sys.setrecursionlimit(1500)
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    labels = set()
    all = []
    for l in lines:
        left, right = l.split(": ")
        right = right.split()
        labels.add(left)

        for r in right:
            all.append((left,r))
            labels.add(r)

    for i, item1 in enumerate(all):
        print("Working on {} of {}".format(i, len(all)))
        for j, item2 in enumerate(all[i+1:]):
            g1 = Graph(len(labels))
            for a in all:
                if (a[0],a[1]) != item1 and (a[1],a[0]) != item1 and (a[0],a[1]) != item2 and (a[1],a[0]) != item2:
                    g1.addEdge(a[0],a[1])

            g1.bridge()
            if len(g1.bridges) == 1:
                print("found {}, {}, {}".format(item1, item2, g1.bridges))



                my_groups = [len(find_all(g1.graph, item1[0], [item1, item2, *g1.bridges])), \
                            len(find_all(g1.graph, item1[1], [item1, item2, *g1.bridges]))]
                acc = 1
                for g in my_groups:
                    acc = acc * g
                print(acc)
                return acc, -1

    return p1,p2


def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0

    map = {}
    all = []
    for l in lines:
        left, right = l.split(": ")
        right = right.split()

        for r in right:
            all.append((left,r))
            # all.append((r,left))

            if left in map.keys():
                map[left].add(r)
            else:
                map[left] = {r}

            if r in map.keys():
                map[r].add(left)
            else:
                map[r] = {left}

    all = list(set(all))

    print("all is ", len(all))

    start=timer()
    all_list = list([a[0] for a in all])

    max_len = 0
    p = [ 0 ]
    a = all_list[0]
    max_pair = ('sdg', 'jfh')
    if len(max_pair) < 2:
        for i, b in enumerate(all_list):
            print(i, " of ", len(all_list))
            p = find_farthest_v2(map, b)
            if len(p) > max_len:
                max_len = len(p)
                a = p[-1]
                print("find furthest from {} is {} len {}".format(b, p[-1], len(p)))
                max_pair = (b,a)
    print("max pair", max_pair, max_len)

    max_len = 0
    paths = []
    start = timer()
    print("finding paths")
    segment_distribution = {}
    one_end = { max_pair[0] }
    print("one end", one_end)

    for i in range(2):
        n_one_end = set()
        for p in one_end:
            n_one_end.update(map[p])
        one_end = n_one_end

    other_end =[ max_pair[1]]
    for i in range(2):
        n_other_end = set()
        for p in one_end:
            n_other_end.update(map[p])
        other_end = n_other_end
    print("one end", one_end)
    print("other end", other_end)
    for i, a in enumerate(one_end):
        print(i, " of ", len(one_end))
        for b in other_end:
            p = find_shortest_path(map, a, b)
            for point_index, point in enumerate(p[:-1]):
                if (point, p[point_index + 1]) in segment_distribution:
                    segment_distribution[(point, p[point_index + 1])] += 1
                elif (p[point_index + 1], point) in segment_distribution:
                    segment_distribution[(p[point_index + 1], point)] += 1
                else:
                    segment_distribution[point, p[point_index + 1]] = 1
        segment_use = sorted(list(segment_distribution.values()), reverse=True)[:5]
        print("Top 5: ", [s for s in sorted([(s,d) for s,d in segment_distribution.items() if d in segment_use],key=lambda z : z[1], reverse=True)][:5], "elapsed ", timer()-start)
        current_tally = [s for s in
                     sorted([(s, d) for s, d in segment_distribution.items() if d in segment_use], key=lambda z: z[1],
                            reverse=True)][0][1]
        print(current_tally)
        if current_tally > 100000:
            break

    print("paths: ", timer()-start, len(paths))

    segment_use = sorted(list(segment_distribution.values()), reverse=True)[:5]
    print("Top 5: ", [s for s in sorted([(s,d) for s,d in segment_distribution.items() if d in segment_use],key=lambda z : z[1], reverse=True)][:5], "elapsed ", timer()-start)
    top_5 = [s[0] for s in sorted([(s,d) for s,d in segment_distribution.items() if d in segment_use],key=lambda z : z[1], reverse=True)][:5]
    print("Top 5 is ", top_5)

    start = timer()
    my_groups = set()

    exclude = top_5
    revised_map = {k: [l for l in i if (k, l) not in exclude and (l, k) not in exclude] for
                   k, i in map.items()}
    result = find_shortest_path(revised_map, *max_pair)
    if result is None:
        print("No path from {} to {} excluding {}".format(*max_pair, exclude))
    else:
        print("Path from {} to {} excluding {} is {}".format(*max_pair, exclude, result))
        print("Path from {} to {} normal is {}".format(*max_pair, find_shortest_path(map, *max_pair)))


    # z = all[0][0]
    # res = find_all(map, z, [a, b, c])
    # print(">>> possible solve", a, b, c)

    for item in top_5:
        print("Item: ", item)
        for z in item:
            res = find_all(revised_map, z, top_5)
            res = tuple(sorted(list(res)))
            my_groups.add(res)
            # print(z,a,b,c)
            # print(res)
            print(len(my_groups))
            if len(my_groups) == 2:
                acc = 1
                for g in my_groups:
                    acc = acc * len(g)
                return acc, -1

    return p1, p2


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


def find_farthest(map, a, exclude):
    open_list = { a }
    result = set()
    low = { a: 0 }

    while open_list:
        m = open_list.pop()

        if m in [k for k, d in map.items() if (k, d) not in exclude and (d, k) not in exclude] and m not in result:
            for n in [d for d in map[m] if (m, d) not in exclude and (d, m) not in exclude]:
                if n not in result:
                    low[n] = low[m] + 1
                    open_list.add(n)

                elif low[n] > low[m] + 1:
                    low[n] = low[m]
                    open_list.add(n)

        result.add(m)

    biggest = [(k, item) for k, item in low.items() if item == max(low.values())]

    if len(biggest) > 0:
        return biggest[0]
    else:
        return a, 0


def find_children(k, map):
    b_found = False
    open_list = {k}
    closed = set()
    while open_list:
        m = open_list.pop()
        if m in map.keys():
            for j in map[m]:
                open_list.add(j)

        closed.add(m)
    return closed


def find_parent(k, map):
    b_found = True
    while b_found:
        for j in map.keys():
            b_found = False
            if k in map[j]:
                k = j
                b_found = True
    return k


# Python program to find bridges in a given undirected graph
# Complexity : O(V+E)

from collections import defaultdict


# This class represents an undirected graph using adjacency list representation
class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph
        self.Time = 0
        self.bridges = []

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    '''A recursive function that finds and prints bridges
    using DFS traversal
    u --> The vertex to be visited next
    visited[] --> keeps track of visited vertices
    disc[] --> Stores discovery times of visited vertices
    parent[] --> Stores parent vertices in DFS tree'''

    def bridgeUtil(self, u, visited, parent, low, disc):
        # Mark the current node as visited and print it
        visited[u] = True

        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1

        # Recur for all the vertices adjacent to this vertex
        for v in self.graph[u]:
            # If v is not visited yet, then make it a child of u
            # in DFS tree and recur for it
            if visited[v] == False:
                parent[v] = u
                self.bridgeUtil(v, visited, parent, low, disc)

                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                low[u] = min(low[u], low[v])

                ''' If the lowest vertex reachable from subtree
                under v is below u in DFS tree, then u-v is
                a bridge'''
                if low[v] > disc[u]:
                    self.bridges.append((u,v))
                    print("{} {}".format(u, v))


            elif v != parent[u]:  # Update low value of u for parent function calls.
                low[u] = min(low[u], disc[v])

    # DFS based function to find all bridges. It uses recursive
    # function bridgeUtil()
    def bridge(self):

        # Mark all the vertices as not visited and Initialize parent and visited,
        # and ap(articulation point) arrays
        visited = {k: False for k in self.graph.keys() }
        disc = {k: float("Inf") for k in self.graph.keys() }
        low = {k: float("Inf") for k in self.graph.keys() }
        parent = {k: -1 for k in self.graph.keys() }

        # Call the recursive helper function to find bridges
        # in DFS tree rooted with vertex 'i'
        for i in self.graph.keys():
            if visited[i] == False:
                self.bridgeUtil(i, visited, parent, low, disc)


# This code is contributed by Neelam Yadav

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
