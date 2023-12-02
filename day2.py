import re
import scrib
import os
from collections import namedtuple

def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    total = 0

    for l in input_lines:
        min_colors = {"red": 0, "green": 0, "blue": 0}
        (game,result) = l.split(": ")
        game_id = scrib.find_int(game)

        results = result.split("; ")
        color_combo_collection = {}

        for r in results:
            color_combos = r.split(", ")
            for cc in color_combos:
                color_combo_collection[cc.split(" ")[1]] = scrib.find_int(cc.split(" ")[0])

            for color in color_combo_collection.keys():
                if min_colors[color] < color_combo_collection[color]:
                    min_colors[color] = color_combo_collection[color]

        total = total + min_colors["red"] * min_colors["blue"] * min_colors["green"]

    return total


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0
    max_colors = {"red": 12, "green": 13, "blue": 14}

    for l in input_lines:
        (game,result) = l.split(": ")
        game_id = scrib.find_int(game)

        results = result.split("; ")
        color_combo_collection = {}
        possible = True
        for r in results:
            color_combos = r.split(", ")
            for cc in color_combos:
                color_combo_collection[cc.split(" ")[1]] = scrib.find_int(cc.split(" ")[0])

            for color in max_colors.keys():
                if color in color_combo_collection.keys() and color_combo_collection[color] > max_colors[color]:
                    possible = False

        if possible:
            total = total + game_id



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