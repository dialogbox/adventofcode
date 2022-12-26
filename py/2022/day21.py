import utils


def parse_input(path):
    lines = utils.read_lines(path)

    monkeys = [l.split(": ") for l in lines]
    simple_monkeys = dict([(m[0], int(m[1])) for m in monkeys
                           if ' ' not in m[1]])
    complex_monkeys = dict([(m[0], m[1].split(" ")) for m in monkeys
                            if ' ' in m[1]])

    return (simple_monkeys, complex_monkeys)


def compute(simple_monkeys, complex_monkeys, monkey):
    if monkey in simple_monkeys:
        return simple_monkeys[monkey]

    if monkey not in complex_monkeys:
        return None

    fomular = complex_monkeys[monkey]

    op1 = compute(simple_monkeys, complex_monkeys, fomular[0])
    op2 = compute(simple_monkeys, complex_monkeys, fomular[2])

    if op1 == None or op2 == None:
        return None

    if fomular[1] == '+':
        return op1 + op2
    if fomular[1] == '-':
        return op1 - op2
    if fomular[1] == '*':
        return op1 * op2
    if fomular[1] == '/':
        return op1 // op2

    print(f"what?? {fomular}")


def part1(path):
    simple_monkeys, complex_monkeys = parse_input(path)

    print(compute(simple_monkeys, complex_monkeys, "root"))


def find_human_value(simple_monkeys, complex_monkeys, root, value):

    cur = root
    cur_value = value

    while True:
        if cur in simple_monkeys:
            raise KeyError(f"{cur} is a simple monkey")

        if cur == "humn":
            return cur_value

        op1, op, op2 = complex_monkeys[cur]
        op1_val = compute(simple_monkeys, complex_monkeys, op1)
        op2_val = compute(simple_monkeys, complex_monkeys, op2)

        next_cur = None
        new_value = None
        if op1_val == None:
            next_cur = op1
            if op == '+':
                new_value = cur_value - op2_val
            elif op == '-':
                new_value = cur_value + op2_val
            elif op == '*':
                new_value = cur_value // op2_val
            elif op == '/':
                new_value = cur_value * op2_val
        elif op2_val == None:
            next_cur = op2
            if op == '+':
                new_value = cur_value - op1_val
            elif op == '-':
                new_value = op1_val - cur_value
            elif op == '*':
                new_value = cur_value // op1_val
            elif op == '/':
                new_value = op1_val // cur_value

        cur = next_cur
        cur_value = new_value


def part2(path):
    simple_monkeys, complex_monkeys = parse_input(path)

    del simple_monkeys['humn']

    op1, _, op2 = complex_monkeys['root']

    op1_val = compute(simple_monkeys, complex_monkeys, op1)
    op2_val = compute(simple_monkeys, complex_monkeys, op2)

    root_monkey = None
    root_value = None
    if op1_val == None:
        root_monkey = op1
        root_value = op2_val
    elif op2_val == None:
        root_monkey = op2
        root_value = op1_val

    print(
        find_human_value(simple_monkeys, complex_monkeys, root_monkey,
                         root_value))
