import re
import scrib as s
import os
from collections import namedtuple
from timeit import default_timer as timer
from collections import deque
import math


m_types = ['%', '&']
def solve(input):
    with open(input) as f:
        lines = f.read().splitlines()

    modules = {}
    inputs = {}

    for l in lines:
        module, destinations = l.split(" -> ")
        if module[0] in m_types:
            m_type, module = (module[0],module[1:])
        else:
            m_type, module = ('broadcaster', module)

        destinations = [n for n in destinations.split(", ")]
        modules[module] = (m_type, destinations)

        for d in destinations:
            if d not in modules.keys():
                modules[d] = (None, [])

            if d in inputs.keys():
                inputs[d].append(module)
            else:
                inputs[d] = [module]

    for m in modules:
        m_type, m_dest = modules[m]

        if m_type == '&':
            modules[m] = (m_type, m_dest, {i: 0 for i in inputs[m]})

        elif m_type == "%":
            modules[m] = (m_type, m_dest, 0)

        else:
            modules[m] = (m_type, m_dest, None)


    print(modules)
    print(inputs)

    hi_count = 0
    lo_count = 0
    p1, p2 = 0, 0
    last = {}
    last_count = {}
    numbers = set()

    for count in range(10000):
        signals = deque()
        m = (0,'button','broadcaster')
        signals.append(m)

        while signals:
            s, from_module, module = signals.popleft()
            m_type = modules[module][0]
            m_dest = modules[module][1]
            m_state = modules[module][2]

            # print(s, from_module, module, modules[module])
            if s == 0:
                lo_count += 1
            else:
                hi_count += 1

            if count == 999:
                p1 = hi_count * lo_count

            # m_state ?
            if module == "rx" and s == 0:
                p2 = count
                return p1, p2

            if m_type == 'broadcaster':
                for d in m_dest:
                    signals.append((s, module, d))

            if m_type == "%":
                if s == 0:
                    if m_state == 0:
                        for d in m_dest:
                            signals.append((1, module, d))
                    else:
                        for d in m_dest:
                            signals.append((0, module, d))
                    m_state = (m_state + 1) % 2
                    modules[module] = (m_type, m_dest, m_state)

            if m_type == "&":
                m_state[from_module] = s
                if all(v == 1 for v in m_state.values()):
                    for d in m_dest:
                        signals.append((0, module, d))
                else:
                    for d in m_dest:
                        signals.append((1, module, d))
                modules[module] = (m_type, m_dest, m_state)

            # if not all([v==0 for v in modules['mg'][2].values()]):
            if modules['mg'][2] != last:
                if len(last) > 0:
                    which_changed = [k for k, v in modules['mg'][2].items() if v != last[k]][0]
                    if which_changed in last_count.keys() and last_count[which_changed] != count:
                        # print(which_changed, count-last_count[which_changed])
                        numbers.add(count-last_count[which_changed])
                    last_count[which_changed] = count

                    if len(numbers) == len(last):
                        p2 = math.lcm(*numbers)
                last = {k:v for k, v in modules['mg'][2].items()}
                # print(count, [(d, modules[d][2]) for d in inputs["rx"]])
    return p1, p2


if __name__ == '__main__':
    d = s.find_filename(__file__)
    d = d[:len(d)-3]

    input_file = "./data/" + d + "_input.txt"
    p1, p2 = solve(input_file)
    print("{} part 1: {}".format(d,p1))
    print("{} part 2: {}".format(d,p2))

    # lst = [1, 4, 4, 4, 2, 5, 6, 6, 7, 8, 9, 10]
    # print(s.find_most_frequent(lst))
    # print(s.find_occurances(lst)[4])
    # print(s.find_even(lst))
    # print(s.capitalize_words(["python", "javaScript", "c++"]))
