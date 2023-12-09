import re
import scrib
import os
from collections import namedtuple
from timeit import default_timer as timer


def load_file(input_lines):
    index = 2
    category = 0
    maps = {}
    lowest_location = -1
    while index < len(input_lines):
        l = input_lines[index]
        while l != "":
            if "map" in l:
                maps[category] = []
            else:
                maps[category].append([int(n) for n in l.split()])
                if category == 6:
                    if maps[category][-1][1] + maps[category][-1][2] > lowest_location:
                        lowest_location = maps[category][-1][1] + maps[category][-1][2]
            index = index + 1
            if index < len(input_lines):
                l = input_lines[index]
            else:
                l = ""
        if index < len(input_lines):
            category = category + 1
        index = index + 1
    return lowest_location, maps


def part2_v2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    seeds = [int(n) for n in input_lines[0].split()[1:]]

    lowest_location, maps = load_file(input_lines)

    location_starts = [maps[len(maps)-1][i][0] for i in range(len(maps[len(maps)-1]))]
    location_starts.sort()
    location_starts.append(lowest_location)

    for each_range in range(len(location_starts)-1):
        num = check_range(maps,seeds,location_starts[each_range], location_starts[each_range+1])

        if num > 0:
            return num

    return lowest_location


def check_range(maps, seeds, start, end):
    step = int((end - start ) / 100)
    if step < 1:
        step = 1

    print("trying {} to {} step {}".format(start,end,step))
    for location in range(start,end,step):
        num = location_to_seed(maps, location)

        for seed_index in range(int(len(seeds) / 2)):
            if num in range(seeds[seed_index * 2], seeds[seed_index * 2] + seeds[seed_index * 2 + 1]):
                if step == 1:
                    return location
                else:
                    return check_range(maps, seeds, location-step,location+1)

    return -1


def location_to_seed(maps, num):
    for c_index in range(len(maps) - 1, -1, -1):
        c = maps[c_index]
        found = False
        old_num = num
        new_num = num
        for r in c:
            if r[0] <= num < r[0] + r[2]:
                new_num = r[1] + num - r[0]
                break

        num = new_num
    return num


def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    seeds = [int(n) for n in input_lines[0].split()[1:]]

    lowest_location, maps = load_file(input_lines)

    for s in seeds:
        num = seed_to_location(maps, s)

        if num < lowest_location:
            lowest_location = num

    return lowest_location


def seed_to_location(maps, num):
    for c in maps.values():
        found = False
        old_num = num
        new_num = num
        for r in c:
            if r[1] <= num < r[1] + r[2]:
                new_num = r[0] + num - r[1]

        num = new_num
    return num


if __name__ == '__main__':
    d = scrib.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    start = timer()
    print("{} part 1: {} in {} seconds".format(d,part1(input_file),timer()-start))
    assert(part1(input_file)==111627841)

    start = timer()
    print("{} part 2: {} in {} seconds".format(d,part2_v2(input_file),timer()-start))
    assert(part2_v2(input_file)==69323688)
    # part 2 answer 69,323,688

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(scrib.find_most_frequent(lst))
    # print(scrib.find_occurances(lst)[4])
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))