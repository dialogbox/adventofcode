from __future__ import annotations


data = [{
    "items": [93, 54, 69, 66, 71],
    "op": lambda o: o * 3,
    "test": lambda i: 7 if i % 7 == 0 else 1
}, {
    "items": [89, 51, 80, 66],
    "op": lambda o: o * 17,
    "test": lambda i: 5 if i % 19 == 0 else 7
}, {
    "items": [90, 92, 63, 91, 96, 63, 64],
    "op": lambda o: o + 1,
    "test": lambda i: 4 if i % 13 == 0 else 3
}, {
    "items": [65, 77],
    "op": lambda o: o + 2,
    "test": lambda i: 4 if i % 3 == 0 else 6
}, {
    "items": [76, 68, 94],
    "op": lambda o: o * o,
    "test": lambda i: 0 if i % 2 == 0 else 6
}, {
    "items": [86, 65, 66, 97, 73, 83],
    "op": lambda o: o + 8,
    "test": lambda i: 2 if i % 11 == 0 else 3
}, {
    "items": [78],
    "op": lambda o: o + 6,
    "test": lambda i: 0 if i % 17 == 0 else 1
}, {
    "items": [89, 57, 59, 61, 87, 55, 55, 88],
    "op": lambda o: o + 7,
    "test": lambda i: 2 if i % 5 == 0 else 5
}]


def parse_input(path):
    return data


def part1(path):
    monkeys = parse_input(path)

    ninspect = [0] * len(monkeys)

    for round in range(20):
        for i, m in enumerate(monkeys):
            ninspect[i] += len(m["items"])
            for item in m["items"]:
                n = m["op"](item) // 3
                next_monkey = m["test"](n)
                monkeys[next_monkey]["items"].append(n)
            m["items"] = []

    ninspect = sorted(ninspect)
    print(ninspect[-1] * ninspect[-2])



def part2(path):
    monkeys = parse_input(path)

    ninspect = [0] * len(monkeys)

    for round in range(10000):
        for i, m in enumerate(monkeys):
            ninspect[i] += len(m["items"])
            for item in m["items"]:
                n = m["op"](item)
                next_monkey = m["test"](n)
                monkeys[next_monkey]["items"].append(n)
            m["items"] = []

    ninspect = sorted(ninspect)
    print(ninspect[-1] * ninspect[-2])