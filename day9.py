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

    total = sum([get_first(nums) for nums in numbers])

    return total


def get_first(my_list):
    occ = scrib.find_occurances(my_list)
    if len(list(occ)) == 1:
        return occ.most_common(1)[0][0]
    else:
        return my_list[0] - get_first([my_list[index+1]-my_list[index] for index in range(len(my_list)-1)])


def get_next(my_list):
    occ = scrib.find_occurances(my_list)
    if len(list(occ)) == 1:
        return occ.most_common(1)[0][0]
    else:
        return my_list[-1] + get_next([my_list[index+1]-my_list[index] for index in range(len(my_list)-1)])


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