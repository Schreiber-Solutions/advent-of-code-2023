import re
import scrib
import os
from collections import namedtuple
import functools


def part2(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    cards = []
    bids = {}

    for l in input_lines:
        cards.append(l.split()[0])
        bids[l.split()[0]] = int(l.split()[1])

    sorted_l = sorted(cards, key=functools.cmp_to_key(compare_v2))

    index = 1
    for c in sorted_l:
        # print(index,c,bids[c])
        total = total + index * bids[c]
        index = index + 1

    return total

def compare_v2(card1,card2):
    if get_type_v2(card1) < get_type_v2(card2):
        return 1
    elif get_type_v2(card1) > get_type_v2(card2):
        return -1
    else:
        return compare_same_types_v2(card1,card2)


def get_type_v2(card):
    occ = scrib.find_occurances(card)
    jokers = occ['J']
    most_frequent = [a for a in occ.most_common() if a[0] != 'J']

    # how_many = [int(n) for n in occ.values()]
    if jokers == 5 or most_frequent[0][1] + jokers == 5:
        return 1
    elif most_frequent[0][1] + jokers == 4:
        return 2
    elif most_frequent[0][1] + jokers == 3 and most_frequent[1][1] == 2:
        return 3
    elif most_frequent[0][1] + jokers == 3:
        return 4
    elif most_frequent[0][1] == 2 and most_frequent[1][1] + jokers == 2:
        return 5
    elif most_frequent[0][1] + jokers == 2:
        return 6
    else:
        return 7


def compare_same_types_v2(card1,card2):
    cards = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

    for index in range(len(card1)):
        if cards.index(card1[index]) < cards.index(card2[index]):
            return 1
        elif cards.index(card1[index]) > cards.index(card2[index]):
            return -1

    return 0

def get_type(card):
    occ = scrib.find_occurances(card)

    most_frequent = occ.most_common()
    # how_many = [int(n) for n in occ.values()]
    if most_frequent[0][1] == 5:
        return 1
    elif most_frequent[0][1] == 4:
        return 2
    elif most_frequent[0][1] == 3 and most_frequent[1][1] == 2:
        return 3
    elif most_frequent[0][1] == 3:
        return 4
    elif most_frequent[0][1] == 2 and most_frequent[1][1] == 2:
        return 5
    elif most_frequent[0][1] == 2:
        return 6
    else:
        return 7


def compare_same_types(card1,card2):
    cards = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    for index in range(len(card1)):
        if cards.index(card1[index]) < cards.index(card2[index]):
            return 1
        elif cards.index(card1[index]) > cards.index(card2[index]):
            return -1

    return 0

def compare(card1,card2):
    if get_type(card1) < get_type(card2):
        return 1
    elif get_type(card1) > get_type(card2):
        return -1
    else:
        return compare_same_types(card1,card2)

def part1(input):
    with open(input) as f:
        input_lines = f.read().splitlines()

    total = 0

    cards = []
    bids = {}

    for l in input_lines:
        cards.append(l.split()[0])
        bids[l.split()[0]] = int(l.split()[1])

    sorted_l = sorted(cards, key=functools.cmp_to_key(compare))

    index = 1
    for c in sorted_l:
        # print(index,c,bids[c])
        total = total + index * bids[c]
        index = index + 1

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
    # print(scrib.find_occurances("A4122"))
    # print(scrib.find_even(lst))
    # print(scrib.capitalize_words(["python", "javaScript", "c++"]))
    # print(scrib.reverse_list(lst))