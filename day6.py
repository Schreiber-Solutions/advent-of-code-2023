import math
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

    t = time
    won = sum([1 for hold_time in range(t+1) if hold_time*(t-hold_time) > distance])
    # print((distance+math.sqrt(t**2-4*distance))/2-(distance-math.sqrt(t**2-4*distance))/2)
    # won = int((distance+math.sqrt(t**2-4*distance))/2-(distance-math.sqrt(t**2-4*distance))/2)
    return won


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    times = [int(n) for n in input_lines[0].split(":")[1].split()]
    distances = [int(n) for n in input_lines[1].split(":")[1].split()]

    total = 1
    for index in range(len(times)):
        t = times[index]
        distance = distances[index]
        won = 0
        for hold_time in range(t+1):
            traveled = hold_time*(t-hold_time)
            if traveled > distance:
                won = won + 1

        # print(won,(distance + math.sqrt(t ** 2 - 4 * distance)) / 2 - (distance - math.sqrt(t ** 2 - 4 * distance)) / 2)
        total = total * won

    return total

if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    print("{} part 1: {}".format(d,part1(input_file)))
    result = part2(input_file)
    assert(result==33875953)
    print("{} part 2: {}".format(d,result))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))