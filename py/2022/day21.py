import utils
import sys
import resource


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


def invert_fomular(complex_monkeys):
    result = {}

    for monkey, fomular in complex_monkeys.items():
        if monkey == 'root':
            continue

        op1, op, op2 = fomular

        if op == '+':
            result[op1] = (monkey, '-', op2)
            result[op2] = (monkey, '-', op1)
        if op == '-':
            result[op1] = (op2, '+', monkey)
            result[op2] = (op1, '-', monkey)
        if op == '/':
            result[op1] = (op2, '*', monkey)
            result[op2] = (op1, '/', monkey)
        if op == '*':
            result[op1] = (monkey, '/', op2)
            result[op2] = (monkey, '/', op1)
        
    return result


def part1(path):
    simple_monkeys, complex_monkeys = parse_input(path)

    print(compute(simple_monkeys, complex_monkeys, "root"))

def part2(path):
    simple_monkeys, complex_monkeys = parse_input(path)

    inverted = invert_fomular(complex_monkeys)
    del simple_monkeys['humn']

    op1, _, op2 = complex_monkeys['root']

    op1_val = compute(simple_monkeys, complex_monkeys, op1)
    op2_val = compute(simple_monkeys, complex_monkeys, op2)

    simple_monkeys["_zero_"] = 0
    if op1_val == None:
        simple_monkeys[op2] = op2_val
        inverted[op1] = (op2, '+', '_zero_')
    elif op2_val == None:
        simple_monkeys[op1] = op1_val
        inverted[op2] = (op1, '+', '_zero_')

    print(compute(simple_monkeys, inverted, "humn"))
