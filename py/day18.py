import math
import utils
import copy


def parse_pair2(input):
    depth = 0

    for c in input:
        if c == '[':
            depth += 1
            continue
        if c == ',':
            continue
        if c == ']':
            depth -= 1
            continue

        yield [depth, int(c)]


def parse_pair(input):
    if input[0] != '[':
        print(f"Expected '[' but got '{input[0]}'\n")
        raise ValueError

    if input[1] == '[':
        (lval, newinput) = parse_pair(input[1:])
        input = newinput
    else:
        lval = int(input[1])
        input = input[2:]

    if input[0] != ',':
        print(f"Expected ',' but got '{input[0]}'\n")
        raise ValueError

    if input[1] == '[':
        (rval, newinput) = parse_pair(input[1:])
        input = newinput
    else:
        rval = int(input[1])
        input = input[2:]

    return ([lval, rval], input[1:])


def leftmost_deeps(pair, depth=0):
    found = []
    if isinstance(pair[0], list):
        t = leftmost_deeps(pair[0], depth+1)
        found.extend(t)

    if isinstance(pair[1], list):
        t = leftmost_deeps(pair[1], depth+1)
        found.extend(t)

    if depth > 4 and isinstance(pair[0], int) and isinstance(pair[1], int):
        return pair

    return found[:2]


def leftmost_pair(pair):
    for i, n in enumerate(pair[:-1]):
        if n[0] > 4 and n[0] == pair[i+1][0]:
            return i

    return None


def explode(pair):
    i = leftmost_pair(pair)
    if i == None:
        return False

    l = pair[i]
    r = pair[i+1]

    if i != 0:
        pair[i-1][1] += l[1]
    if i != len(pair)-2:
        pair[i+2][1] += r[1]

    del pair[i]
    pair[i][0] -= 1
    pair[i][1] = 0

    return True


def split(pair):
    for i in range(len(pair)):
        if pair[i][1] >= 10:
            depth = pair[i][0]+1
            lval = [depth, math.floor(pair[i][1]/2)]
            rval = [depth, math.ceil(pair[i][1]/2)]
            pair[i] = rval
            pair.insert(i, lval)
            return True
    return False


def add(left, right):
    for n in left:
        n[0] += 1
    for n in right:
        n[0] += 1

    result = []
    result.extend(left)
    result.extend(right)

    return result


def magnitude(expr):
    while len(expr) > 1:
        idx = 0
        for i, n in enumerate(expr[:-1]):
            if n[0] == expr[i+1][0]:
                idx = i
                break
        expr[i][1] = expr[i][1] * 3 + expr[i+1][1] * 2
        expr[i][0] -= 1
        del expr[i+1]

    return expr[0][1]


def reduce(expr):
    while True:
        exploded = explode(expr)
        if not exploded:
            splitted = split(expr)

        if not exploded and not splitted:
            break


def part1(data):
    cur = data[0]
    for l in data[1:]:
        cur = add(cur, l)
        reduce(cur)

    return magnitude(cur)


def part2(data):
    result = []
    nexpr = len(data)
    n = 0
    for i in range(nexpr):
        for j in range(nexpr):
            cur = add(copy.deepcopy(data[i]), copy.deepcopy(data[j]))
            reduce(cur)
            m = magnitude(cur)
            result.append(m)
            n += 1
    return max(result)


if __name__ == '__main__':
    lines = utils.read_lines("inputs/day18.txt")

    data = [list(parse_pair2(line)) for line in lines]

    m = part1(copy.deepcopy(data))
    print(f"Part 1: {m}")

    m = part2(copy.deepcopy(data))
    print(f"Part 2: {m}")
