import math
import re
import scrib
import os
from collections import namedtuple
from timeit import default_timer as timer

def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    time = int("".join([n for n in input_lines[0].split(":")[1].split()]))
    distance = int("".join([n for n in input_lines[1].split(":")[1].split()]))

    t = time
    # won = sum([1 for hold_time in range(t+1) if hold_time*(t-hold_time) > distance])
    return solve(time,distance)

def solve(time,distance):
    num1 = (time - math.sqrt(time ** 2 - 4 * distance)) / 2
    num2 = (time + math.sqrt(time ** 2 - 4 * distance)) / 2

    # print(num1,num2)
    # print([hold_time for hold_time in range(time + 1) if hold_time * (time - hold_time) > distance])
    # print([hold_time for hold_time in range(math.floor(num1), math.ceil(num2) + 1) if hold_time * (time - hold_time) > distance])
    # won = sum([1 for hold_time in range(time + 1) if hold_time * (time - hold_time) > distance])

    won = sum([1 for hold_time in range(math.floor(num1),math.ceil(num2)+1) if hold_time * (time - hold_time) > distance])
    # won = sum([1 for hold_time in range(time+1) if hold_time * (time - hold_time) > distance])

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
        won = solve(t,distance)
        total = total * won

    return total

if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    print("{} part 1: {}".format(d,part1(input_file)))
    assert(part1(input_file)==281600)
    result = part2(input_file)
    assert(result==33875953)
    print("{} part 2: {}".format(d,result))
    print("Elapsed time {}".format(timer()-start))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))