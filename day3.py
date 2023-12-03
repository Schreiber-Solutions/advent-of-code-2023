import re
import scrib
import os
from collections import namedtuple

def is_gear_adjacent(g,row,col):
    for r_o in [-1,0,1]:
        for c_o in [-1,0,1]:
            if get_item(g,row+r_o,col+c_o) == '*':
                return (row+r_o,col+c_o)

    return (-1,-1)


def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    row = 0
    max_rows = len(input_lines)
    grid = {}
    max_cols = len(input_lines[0])
    for l in input_lines:
        col = 0
        for c in l:
            grid[(row,col)] = c
            col = col + 1
        row = row + 1

    gears = {}

    for row in range(max_rows):
        num = ""
        is_symbol = False
        location = (-1,-1)

        for col in range(max_cols):
            c = grid[(row,col)]
            if c.isnumeric():
                num = num + c
                if is_gear_adjacent(grid,row,col) != (-1,-1):
                    is_symbol = True
                    location = is_gear_adjacent(grid,row,col)

            else:
                if num.isnumeric() and is_symbol:
                    if location in gears.keys():
                        gears[location].append(num)
                    else:
                        gears[location] = [num]

                    # print("found gear at {}".format(location))

                num = ""
                is_symbol = False

    for g in gears.keys():
        if len(gears[g]) > 1:
            # print("location {} has {}".format(g,gears[g]))
            num = 1
            for n in gears[g]:
                num = num * int(n)

            total = total + num

    return total

def get_item(g,row,col):
    if (row,col) in g.keys():
        return g[(row,col)]
    else:
        return "."

def is_symbol_adjacent(g,row,col):
    for r_o in [-1,0,1]:
        for c_o in [-1,0,1]:
            if get_item(g,row+r_o,col+c_o) not in ['0','1','2','3','4','5','6','7','8','9','.']:
                return True

    return False


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    row = 0
    max_rows = len(input_lines)
    grid = {}
    max_cols = len(input_lines[0])
    for l in input_lines:
        col = 0
        for c in l:
            grid[(row,col)] = c
            col = col + 1
        row = row + 1


    for row in range(max_rows):
        num = ""
        is_symbol = False

        for col in range(max_cols):
            c = grid[(row,col)]
            if c.isnumeric():
                num = num + c
                if is_symbol_adjacent(grid,row,col):
                    is_symbol = True
            else:
                if num.isnumeric() and is_symbol:
                    total = total + int(num)

                num = ""
                is_symbol = False


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