import utils
import math


def parse_input(path):
    inputstr = utils.readall(path)

    result = []

    for mstr in inputstr.split("\n\n"):
        temp = [l.split(": ")[1] for l in mstr.split("\n")[1:]]
        items = [int(i) for i in temp[0].split(", ")]
        opstr = temp[1].strip()
        op = opstr
        test_data = [int(l.split()[-1]) for l in temp[2:]]

        result.append((items, op, test_data))

    return result


def run_op(op, old):
    ldict = {"old": old, "new": 0}
    exec(op, globals(), ldict)
    # print(op, old, ldict["new"])
    return ldict["new"]


def do_round(status, ninspect, manage_worry):
    for i, m in enumerate(status):
        ninspect[i] += len(m[0])
        for item in m[0]:
            n = manage_worry(run_op(m[1], item))
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
