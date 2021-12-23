from itertools import product

lines = open("inputs/day22.txt", "r").read().splitlines()
input = [
    (op[0], tuple([c.split("=")[1].split("..") for c in op[1].split(",")]))
    for op in [line.split() for line in lines]
]
input = [
    (op[0], tuple([(int(axis[0]), int(axis[1])) for axis in op[1]])) for op in input
]


def is_fully_contained(c1, c2):
    (x1, y1, z1) = c1
    (x2, y2, z2) = c2

    points2 = list(product([x2[0], x2[1]], [y2[0], y2[1]], [z2[0], z2[1]]))

    for (x, y, z) in points2:
        if not (
            x1[0] <= x
            and x1[1] >= x
            and y1[0] <= y
            and y1[1] >= y
            and z1[0] <= z
            and z1[1] >= z
        ):
            return False
    return True


def is_valid_range(r):
    if r[0] > r[1]:
        return False
    return True


def diff_range(r1, r2):
    prefix = tuple([r1[0], r2[0] - 1])
    overwrap = tuple([max(r1[0], r2[0]), min(r1[1], r2[1])])
    postfix = tuple([r2[1] + 1, r1[1]])

    result = ([], [])

    if is_valid_range(prefix):
        result[0].append(prefix)

    if is_valid_range(postfix):
        result[0].append(postfix)

    if is_valid_range(overwrap):
        result[1].append(overwrap)

    return result


def diff_cubes(c1, c2):
    if is_fully_contained(c2, c1):
        return set()

    (x1, y1, z1) = c1
    (x2, y2, z2) = c2

    xdiff = diff_range(x1, x2)
    ydiff = diff_range(y1, y2)
    zdiff = diff_range(z1, z2)

    if len(xdiff[1]) == 0 or len(ydiff[1]) == 0 or len(zdiff[1]) == 0:
        return set([c1])

    all_slices = list(
        product(xdiff[0] + xdiff[1], ydiff[0] + ydiff[1], zdiff[0] + zdiff[1])
    )[:-1]
    all_slices_set = set(all_slices)

    return all_slices_set


def turn_on(state, c1):
    new_state = turn_off(state, c1)

    new_state.add(c1)

    return new_state


def turn_off(state, c1):
    new_state = set()
    for c in state:
        diffs = diff_cubes(c, c1)
        new_state = new_state.union(diffs)

    return new_state


turnedon = set()

for op in input:
    if op[0] == "on":
        turnedon = turn_on(turnedon, op[1])
    elif op[0] == "off":
        turnedon = turn_off(turnedon, op[1])

total = 0

for c in sorted(list(turnedon)):
    (x, y, z) = c
    size = (x[1] - x[0] + 1) * (y[1] - y[0] + 1) * (z[1] - z[0] + 1)
    total += size

print(total)
