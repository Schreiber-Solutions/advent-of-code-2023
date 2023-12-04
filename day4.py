import re
import scrib
import os
from collections import namedtuple


def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    cards = [1 for i in range(len(input_lines))]

    for l in input_lines:
        (a,b) = l.split(" | ")
        card = scrib.find_int(a.split(": ")[0])
        winners = [int(n) for n in a.split(": ")[1].split()]
        my_numbers = [int(n) for n in b.split()]

        points = 0
        for w in winners:
            if w in my_numbers:
                points = points + 1

        for p in range(points):
            cards[card+p] = cards[card+p] + cards[card-1]

    return sum(cards)


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    for l in input_lines:
        (a,b) = l.split(" | ")
        winners = [int(n) for n in a.split(": ")[1].split()]
        my_numbers = [int(n) for n in b.split()]

        points = 0
        for w in winners:
            if w in my_numbers:
                if points == 0:
                    points = 1
                else:
                    points = points * 2

        total = total + points

    return total


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    print("{} part 1: {}".format(d,part1(input_file)))
    print("{} part 2: {}".format(d,part2(input_file)))
    # print("day 8 part 1: {}".format(part1("./data/day10_test.txt")))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))