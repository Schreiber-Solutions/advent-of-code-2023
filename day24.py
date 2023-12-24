import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer
from sympy import symbols, Eq, solve

def intersect_3d(line1, line2):
    b_x, b_y, b_z = line1[0]
    b_vx, b_vy, b_vz = line1[1]
    a_x, a_y, a_z = line2[0]
    a_vx, a_vy, a_vz = line2[1]

    mu = (a_y-b_y+(a_vy/a_vx)*(b_x-a_x))/(b_vy-a_vy*b_vx/a_vx)
    l = (b_x + mu*b_vx - a_x)/a_vx

    x = a_x+l*a_vx
    y = a_y+l*a_vy
    z = a_z+l*a_vz

    xp = b_x+mu*b_vx
    yp = b_y+mu*b_vy
    zp = b_z+mu*b_vz

    if z == zp:
        return(xp,yp,zp,mu)
    else:
        return None
def intersect(line1, line2):
    a1,b1,c1 = line1
    a2,b2,c2 = line2
    if (a1*b2-a2*b1) != 0 and (a1*b2-a2*b1) != 0:
        x = (b1*c2-b2*c1)/(a1*b2-a2*b1)
        y = (a2*c1 - a1*c2)/(a1*b2-a2*b1)

        return x,y
    else:
        return None

def my_solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    p1, p2 = 0, 0
    asteroids = []
    for l in lines:
        position, velocity = l.split(" @ ")
        position = [int(n) for n in position.split(", ")]
        velocity = [int(n) for n in velocity.split(", ")]
        asteroids.append((position, velocity))
    test_min = 7 # 200000000000000
    test_max = 27 # 400000000000000

    # test_min = 200000000000000
    # test_max = 400000000000000

    for index, a in enumerate(asteroids):
        for b in asteroids[index+1:]:
            b_x, b_y, b_z = b[0]
            b_vx, b_vy, b_vz = b[1]
            a_x, a_y, a_z = a[0]
            a_vx, a_vy, a_vz = a[1]
            point = intersect((-a_vy, a_vx, a_x*a_vy-a_y*a_vx), (-b_vy, b_vx, b_x*b_vy-b_y*b_vx))

            t1, t2 = symbols('t1,t2')
            eq1 = Eq(b_x+b_vx*t1, a_x+a_vx*t2)
            eq2 = Eq(b_y+b_vy*t1, a_y+a_vy*t2)
            s = solve((eq1, eq2), (t1, t2))

            if point:
                x,y = point
                x = b_x + b_vx * s[t1]
                y = b_y + b_vy * s[t2]
                # print(s)
                # print(a,b,x,y)
                if test_min <= x <= test_max and test_min <= y <= test_max:
                    t1 = s[t1]
                    t2 = s[t2]

                    if t1 > 0 and t2 > 0:
                        print(">>>>> ",b_x, b_y, a_x, a_y, t1, t2)
                        p1 += 1

    # a, b, c = asteroids[:3]
    # b_x, b_y, b_z = b[0]
    # b_vx, b_vy, b_vz = b[1]
    # a_x, a_y, a_z = a[0]
    # a_vx, a_vy, a_vz = a[1]
    # c_x, c_y, c_z = c[0]
    # c_vx, c_vy, c_vz = c[1]

    x, y, z, vx, vy, vz = symbols('x,y,z,vx,vy,vz')
    equations = []
    for a in asteroids:
        a_x, a_y, a_z = a[0]
        a_vx, a_vy, a_vz = a[1]
        eq1 = Eq((a_x-x)*(vy-a_vy),(a_y-y)*(vx-a_vx))
        eq2 = Eq((a_y-y)*(vz-a_vz),(a_z-z)*(vy-a_vy))
        equations.append(eq1)
        equations.append(eq2)

    # eq3 = Eq((b_x-x)*(vy-b_vy),(b_y-y)*(vx-b_vx))
    # eq4 = Eq((b_y-y)*(vz-b_vz),(b_z-z)*(vy-b_vy))
    #
    # eq5 = Eq((c_x-x)*(vy-c_vy),(c_y-y)*(vx-c_vx))
    # eq6 = Eq((c_y-y)*(vz-c_vz),(c_z-z)*(vy-c_vy))

    p2 = solve(equations, (x, y, z, vx, vy, vz))[0]
    print("Solutions ", p2)
    p2 = sum(p2[:3])
    # rock = [(24, 13, 10),(-3, 1, 2)]
    # for b in asteroids:
    #     print(intersect_3d(rock, b))
    return p1, p2


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = my_solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
