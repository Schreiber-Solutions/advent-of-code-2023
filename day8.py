import re
import scrib
import os
from collections import namedtuple

def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    map = {}
    for index in range(2,len(input_lines)):
        l = input_lines[index]
        map[l.split(" = ")[0]] = l.split(" = ")[1].split(", ")
        map[l.split(" = ")[0]][0] = map[l.split(" = ")[0]][0][1:]
        map[l.split(" = ")[0]][1] = map[l.split(" = ")[0]][1][:-1]

        # print(map[l.split(" = ")[0]])

    instructions = input_lines[0]

    next = [k for k in map.keys() if k[-1] == 'A']
    which = {}
    while len(which) < len(next):
        for i in instructions:
            if i == "L":
                next = [map[k][0] for k in next]
            else:
                next = [map[k][1] for k in next]

            total = total + 1
            if (len([n for n in next if n[-1] == "Z"]) == 1):
                matches = [n for n in next if n[-1] == "Z"]
                which[next.index(matches[0])] = total
                # print(next,len([n for n in next if n[-1] == "Z"]))

            if len(next) == (len([n for n in next if n[-1] == "Z"])):
                return total

    factors = []
    for w in which.values():
        # print("w is {}".format(w))
        l = get_prime_factors(w)
        # print("l is {}".format(l))
        factors.extend(l)

    factors = list(set(factors))
    total = 1
    for f in factors:
        total = total * f

    return total


def get_prime_factors(n):
    i = 2
    prime_factors = []
    while i * i <= n:
        if n % i == 0:
            prime_factors.append(i)
            n //= i
        else:
            i += 1

    if n > 1:
        prime_factors.append(n)

    return prime_factors
def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    map = {}
    for index in range(2,len(input_lines)):
        l = input_lines[index]
        # print(l)
        map[l.split(" = ")[0]] = l.split(" = ")[1].split(", ")
        map[l.split(" = ")[0]][0] = map[l.split(" = ")[0]][0][1:]
        map[l.split(" = ")[0]][1] = map[l.split(" = ")[0]][1][:-1]

        # print(map[l.split(" = ")[0]])

    instructions = input_lines[0]

    next = "AAA"

    while next != "ZZZ":
        for i in instructions:
            if i == "L":
                next = map[next][0]
            else:
                next = map[next][1]
            total = total + 1

            if next == "ZZZ":
                return total
    return total

if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    print("{} part 1: {}".format(d,part1(input_file)))
    print("{} part 2: {}".format(d,part2(input_file)))

