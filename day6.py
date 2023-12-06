import re
import scrib
import os
from collections import namedtuple

def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    time = int("".join([n for n in input_lines[0].split(":")[1].split()]))
    distance = int("".join([n for n in input_lines[1].split(":")[1].split()]))

    total = 1

    t = time
    won = 0
    for hold_time in range(t+1):
        traveled = hold_time*(t-hold_time)
        if traveled > distance:
            won = won + 1

        # if hold_time/100000 == int(hold_time/100000):
        #     print("at hold time {}".format(hold_time))
    total = total * won

    return total


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    times = [int(n) for n in input_lines[0].split(":")[1].split()]
    distances = [int(n) for n in input_lines[1].split(":")[1].split()]

    print(times)
    total = 1
    for index in range(len(times)):
        t = times[index]
        won = 0
        for hold_time in range(t+1):
            traveled = hold_time*(t-hold_time)
            if traveled > distances[index]:
                won = won + 1
        print("{} wins {} times".format(index,won))
        total = total * won

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