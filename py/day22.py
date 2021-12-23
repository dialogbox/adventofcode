from itertools import product
import numpy as np

lines = open("inputs/day22.txt", "r").read().splitlines()
input = [
    (op[0], tuple([c.split("=")[1].split("..") for c in op[1].split(",")]))
    for op in [line.split() for line in lines]
]
input = [(op[0], [[int(c) for c in axis] for axis in op[1]]) for op in input]


def gen_cuboid(input):
    for (ops, (x, y, z)) in input:
        if (
            x[0] < -50
            or x[1] > 50
            or y[0] < -50
            or y[1] > 50
            or z[0] < -50
            or z[1] > 50
        ):
            continue

        cuboid = product(
            list(range(x[0], x[1] + 1)),
            list(range(y[0], y[1] + 1)),
            list(range(z[0], z[1] + 1)),
        )
        yield (ops, set([point for point in cuboid]))


def diff(c1, c2):
    nrows, ncols = c1.shape
    dtype = {
        "names": ["f{}".format(i) for i in range(ncols)],
        "formats": ncols * [c1.dtype],
    }

    nc = np.setdiff1d(c1.view(dtype), c2.view(dtype))
    return nc.view(c1.dtype).reshape(-1, ncols)


def union(c1, c2):
    nrows, ncols = c1.shape
    dtype = {
        "names": ["f{}".format(i) for i in range(ncols)],
        "formats": ncols * [c1.dtype],
    }

    nc = np.union1d(c1.view(dtype), c2.view(dtype))
    return nc.view(c1.dtype).reshape(-1, ncols)


cuboids = gen_cuboid(input)

current = set()

for c in cuboids:
    if c[0] == "on":
        current = current | c[1]
    elif c[0] == "off":
        current = current - c[1]

print(len(current))
