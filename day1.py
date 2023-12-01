import re
import scrib
import os
from collections import namedtuple

def find_number(input):
    num = -1

    list = ['0','1','2','3','4','5','6','7','8','9','zero','one','two','three','four','five','six','seven','eight','nine']
    v = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9]

    for c in list:
        if c in input:
            where = input.index(c)
            num = v[list.index(c)]

    return num


def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    for l in input_lines:
        num = ""

        for i in range(len(l)):
            if find_number(l[:i+1]) >= 0:
                num = num + str(find_number(l[:i+1]))
                break

        for i in range(len(l),0,-1):
            if find_number(l[i-1:]) >= 0:
                num = num + str(find_number(l[i-1:]))
                break

        total = total + int(num)

    return total


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    for l in input_lines:
        num = ""
        for c in l:

            if c in ['0','1','2','3','4','5','6','7','8','9']:
                num = num + c
                break

        for c in reversed(l):
            if c in ['0','1','2','3','4','5','6','7','8','9']:
                num = num + c
                break

        total = total + int(num)

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