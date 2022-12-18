import utils
import numpy as np
import itertools


def parse_input(path):
    return utils.read_numbers_csv(path)


def count_open_surface_single_axis(cubes):
    sorted_cubes = cubes[np.lexsort((cubes[:, 2], cubes[:, 1], cubes[:, 0]))]
    groups = itertools.groupby([((c[0], c[1]), c[2]) for c in sorted_cubes],
                               key=lambda x: x[0])
    depthset = [(g[0], set([p[1] for p in g[1]])) for g in groups]

    nsurfaces = 0
    n = 0
    for p, s in depthset:
        for d in s:
            n += 1
            if d + 1 not in s:
                nsurfaces += 1
            if d - 1 not in s:
                nsurfaces += 1

    return nsurfaces


def count_external_surface_single_axis(cubes):
    sorted_cubes = cubes[np.lexsort((cubes[:, 2], cubes[:, 1], cubes[:, 0]))]
    groups = itertools.groupby([((c[0], c[1]), c[2]) for c in sorted_cubes],
                               key=lambda x: x[0])
    depthset = [(g[0], set([p[1] for p in g[1]])) for g in groups]

    nsurfaces = 0
    n = 0
    spaces = []
    for coord, s in depthset:
        s = sorted(s)
        for p1, p2 in zip(s[:-1], s[1:]):
            if p1 + 1 < p2:
                spaces.extend([(coord[0], coord[1], p)
                               for p in range(p1 + 1, p2)])

        for d in s:
            n += 1
            if d + 1 not in s:
                nsurfaces += 1
            if d - 1 not in s:
                nsurfaces += 1

    return nsurfaces, spaces


def exposed_airs(cubeset, airset):
    result = []
    for (x, y, z) in airset:
        closed = set([
            (x - 1, y, z),
            (x + 1, y, z),
            (x, y - 1, z),
            (x, y + 1, z),
            (x, y, z - 1),
            (x, y, z + 1),
        ]) & (cubeset | airset)

        if len(closed) != 6:
            result.append((x, y, z))
    return set(result)


def remove_exposed_air(cubeset, airset):
    while True:
        exposed = exposed_airs(cubeset, airset)
        if len(exposed) == 0:
            return airset
        airset = set([a for a in airset if a not in exposed])


def part1(path):
    data = np.array(parse_input(path))

    n = 0
    n += count_open_surface_single_axis(data[:, (0, 1, 2)])
    n += count_open_surface_single_axis(data[:, (0, 2, 1)])
    n += count_open_surface_single_axis(data[:, (1, 2, 0)])

    print(n)


#
# all open surfaces - all open surfaces of "inner air-cubes"
# remove all air cubes which any of 6 neibour neither cube nor air
#  which means the air cube meets the external world. Remove those one by one
#  until there is no such air cubes
#
def part2(path):
    cubes = parse_input(path)
    data = np.array(cubes)
    cubeset = set([tuple(c) for c in cubes])

    totaln = 0
    inner_spaces1 = None
    inner_spaces2 = None
    inner_spaces3 = None
    n, spaces = count_external_surface_single_axis(data[:, (0, 1, 2)])
    totaln += n
    if spaces != []:
        inner_spaces1 = np.array(spaces)
    n, spaces = count_external_surface_single_axis(data[:, (0, 2, 1)])
    totaln += n
    if spaces != []:
        inner_spaces2 = np.array(spaces)[:, (0, 2, 1)]
    n, spaces = count_external_surface_single_axis(data[:, (1, 2, 0)])
    totaln += n
    if spaces != []:
        inner_spaces3 = np.array(spaces)[:, (2, 0, 1)]

    airset = set(
        set([tuple(l) for l in inner_spaces1])
        & set([tuple(l) for l in inner_spaces2])
        & set([tuple(l) for l in inner_spaces3]))

    airset = remove_exposed_air(cubeset, airset)
    air = np.array(list(airset))

    airn = 0
    airn += count_open_surface_single_axis(air[:, (0, 1, 2)])
    airn += count_open_surface_single_axis(air[:, (0, 2, 1)])
    airn += count_open_surface_single_axis(air[:, (1, 2, 0)])

    print(totaln - airn)