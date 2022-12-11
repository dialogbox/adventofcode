import utils
import math


def parse_input(path):
    inputstr = utils.readall(path)

    result = []

    for mstr in inputstr.split("\n\n"):
        temp = [l.split(": ")[1] for l in mstr.split("\n")[1:]]
        items = [int(i) for i in temp[0].split(", ")]
        [op1, op2] = temp[1].split()[3:]
        op = ("^", 2) if op2 == "old" else (op1, int(op2))

        test_data = [int(l.split()[-1]) for l in temp[2:]]

        result.append((items, op, test_data))

    return result


def do_round(status, ninspect, manage_worry):
    for i, m in enumerate(status):
        ninspect[i] += len(m[0])
        for item in m[0]:
            (op1, op2) = m[1]
            n = 0
            if op1 == "+":
                n = item + op2
            elif op1 == "*":
                n = item * op2
            elif op1 == "^":
                n = item * item
            n = manage_worry(n)
            (divd, tv, fv) = m[2]
            next_monkey = tv if n % divd == 0 else fv
            status[next_monkey][0].append(n)
        m[0].clear()


def part1(path):
    status = parse_input(path)

    ninspect = [0] * len(status)

    for round in range(20):
        do_round(status, ninspect, lambda n: n // 3)

    print(math.prod(sorted(ninspect)[-2:]))


def part2(path):
    status = parse_input(path)

    ninspect = [0] * len(status)

    lcm = math.prod([m[2][0] for m in status])

    for _ in range(10000):
        do_round(status, ninspect, lambda n: n % lcm)

    print(math.prod(sorted(ninspect)[-2:]))
