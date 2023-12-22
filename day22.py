import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer


def take_z(elem):
    return(elem[0][2])

def overlaps(layer, brick):
    for b in layer:
        s_x, s_y, s_z = b[0]
        e_x, e_y, e_z = b[1]

        if ((brick[0][0] >= s_x and brick[0][0] <= e_x) or (brick[1][0] >= s_x and brick[1][0] <= e_x) or \
                (brick[0][0] < s_x and brick[1][0] > e_x) or (brick[0][0] > s_x and brick[1][0] < e_x)) and \
                ( (brick[0][1] >= s_y and brick[0][1] <= e_y) or (brick[1][1] >= s_y and brick[1][1] <= e_y) or \
                    (brick[0][1] < s_y and brick[1][1] > e_y) or (brick[0][1] > s_y and brick[1][1] < e_y) ):
            return True

    return False
def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    bricks = []

    for l in lines:
        s, e = l.split("~")
        s = tuple([int(n) for n in s.split(",")])
        e = tuple([int(n) for n in e.split(",")])
        bricks.append((s,e))

    bricks.sort(key=take_z)
    p1, p2 = 0, 0

    layers, max_z = fell_bricks(bricks)

    # print_layers(layers)

    base_layer = layers.copy()

    # for each_brick in range(len(bricks)):
    for each_brick in range(len(bricks)):
        layers, max_z = fell_bricks([b for index, b in enumerate(bricks) if index != each_brick])
        b_fell = set()
        b_same = True
        print("Testing {}".format(bricks[each_brick]))
        for z, l in enumerate(base_layer):
            for b in l:
                if b not in layers[z] and b != bricks[each_brick]:
                    b_same = False
                    b_fell.add(b)

        if b_same:
            p1 += 1
            print("Brick {} - {} can be removed".format(each_brick, bricks[each_brick]))
        else:
            p2 += len(b_fell)
            print("Brick {} made {} bricks fall".format(each_brick, len(b_fell)))

    return p1, p2
    # 1172 too high


def print_layers(layers):
    for i, l in enumerate(layers):
        if len(l) > 0:
            print(i, l)


def fell_bricks(bricks):
    max_z = 1000
    layers = []
    for i in range(max_z):
        layers.append([])
    for b in bricks:
        b_placed = False
        for z in range(max_z - 1, -1, -1):
            if not b_placed and overlaps(layers[z], b):
                for i in range(b[1][2] - b[0][2] + 1):
                    layers[z + i + 1].append(b)
                b_placed = True
            if not b_placed and z == 0:
                for i in range(b[1][2] - b[0][2] + 1):
                    layers[z + i].append(b)
                b_placed = True
    return layers, max_z


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))

