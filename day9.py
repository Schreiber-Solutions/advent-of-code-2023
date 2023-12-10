import re
import scrib
import os
from collections import namedtuple


def parse(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    numbers = []
    for l in input_lines:
        numbers.append([int(n) for n in l.split()])

    return numbers


def part2(input):
    numbers = parse(input)

    total = sum([get_next(nums) for nums in numbers if nums.reverse() is None])

    return total


def get_next(my_list):
    l = my_list
    t = my_list[-1]
    while not all([n == 0 for n in l]):
        l = [l[i+1]-l[i] for i in range(len(l)-1)]
        t = t + l[-1]
    return t


def part1(input):
    numbers = parse(input)

    total = sum([get_next(nums) for nums in numbers])

    return total


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    print("{} part 1: {}".format(d,part1(input_file)))
    assert(part1(input_file)==2005352194)
    print("{} part 2: {}".format(d,part2(input_file)))
    assert(part2(input_file)==1077)
    # print("day 8 part 1: {}".format(part1("./data/day10_test.txt")))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))