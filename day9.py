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

    total = 0
    current_list = []
    for list_of_numbers in numbers:
        current_list = list_of_numbers
        iterations = 0
        previous_lists = [current_list]
        occ = scrib.find_occurances(current_list)
        while len(list(occ)) > 1 and occ.most_common(1) != 0:
            new_list = [current_list[index+1]-current_list[index] for index in range(len(current_list)-1)]
            previous_lists.append(new_list)
            occ = scrib.find_occurances(new_list)
            iterations = iterations + 1
            current_list = new_list

        # previoius_lists is a history
        first_num = 0
        for list_index in range(len(previous_lists)-2,-1,-1):
            first_num = previous_lists[list_index][0] -previous_lists[list_index+1][0]
            previous_lists[list_index].insert(0,first_num)

        total = total + previous_lists[0][0]

    return total


def part1(input):
    numbers = parse(input)

    total = 0

    current_list = []
    for list_of_numbers in numbers:
        current_list = list_of_numbers
        iterations = 0
        previous_lists = [current_list]
        occ = scrib.find_occurances(current_list)
        while len(list(occ)) > 1 and occ.most_common(1) != 0:
            new_list = [current_list[index+1]-current_list[index] for index in range(len(current_list)-1)]
            previous_lists.append(new_list)
            occ = scrib.find_occurances(new_list)
            iterations = iterations + 1
            current_list = new_list

        # previoius_lists is a history
        next_num = 0
        for list_index in range(len(previous_lists)-2,-1,-1):
            next_num = previous_lists[list_index+1][-1] + previous_lists[list_index][-1]
            previous_lists[list_index].append(next_num)

        total = total + previous_lists[0][-1]
        # print(previous_lists)
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