import utils
import numpy as np


def parse_input(path):
    lines = utils.read_lines(path)

    lines = [
        l.replace("Sensor at ",
                  "").replace(" closest beacon is at ",
                              "").replace(" ", "").replace("x=", "").replace(
                                  "y=", "").split(":") for l in lines
    ]
    sensors = [(utils.parse_coord_str(l[0]), utils.parse_coord_str(l[1]))
               for l in lines]

    return sensors


def get_area(s, b):
    (sx, sy) = s
    (bx, by) = b

    mdist = abs(sx - bx) + abs(sy - by)

    return ((sx - mdist, sx + mdist), (sy - mdist, sy + mdist))


def remove_duplicated_ranges(ranges):
    if len(ranges) == 0:
        return []

    ranges.sort()

    f, t = ranges[0]
    result = [(f, t)]
    for r in ranges:
        if r[1] <= t:
            continue

        if r[0] <= t:
            f = t + 1
            t = r[1]
        else:
            f, t = r

        result.append((f, t))

    compact_result = []
    f = result[0][0]
    t = f - 1
    for r in result:
        if r[0] == t + 1:
            t = r[1]
        else:
            compact_result.append((f, t))
            f, t = r

    compact_result.append((f, t))

    return compact_result


def count_safe_area(sensor_areas, y):
    matching_sensors = [(s, a) for (s, a) in sensor_areas
                        if a[1][0] <= y and a[1][1] >= y]

    ranges = []

    for (s, a) in matching_sensors:
        mdist = a[0][1] - s[0]
        ydist = abs(y - s[1])
        xdist = mdist - ydist

        ranges.append((s[0] - xdist, s[0] + xdist))

    return ranges


def num_beacons_in_ranges(sensors, ranges, y):
    bxs = set([b[0] for (_, b) in sensors if b[1] == y])

    n = 0
    for x in bxs:
        for rf, rt in ranges:
            if x >= rf and x <= rt:
                n += 1

    return n


def part1test(path):
    sensors = parse_input(path)
    sensor_areas = [(s[0], get_area(s[0], s[1])) for s in sensors]

    ranges = count_safe_area(sensor_areas, 10)

    ranges = remove_duplicated_ranges(ranges)

    n_beacons_in_y = num_beacons_in_ranges(sensors, ranges, 10)
    print(n_beacons_in_y)
    print(ranges)
    print(sum([r[1] - r[0] + 1 for r in ranges]) - n_beacons_in_y)


def part1(path):
    sensors = parse_input(path)
    sensor_areas = [(s[0], get_area(s[0], s[1])) for s in sensors]

    ranges = count_safe_area(sensor_areas, 2000000)

    ranges = remove_duplicated_ranges(ranges)

    n_beacons_in_y = num_beacons_in_ranges(sensors, ranges, 2000000)
    print(n_beacons_in_y)
    print(sum([r[1] - r[0] + 1 for r in ranges]) - n_beacons_in_y)


def part2(path):
    sensors = parse_input(path)
    sensor_areas = [(s[0], get_area(s[0], s[1])) for s in sensors]

    for y in range(4000000):
        ranges = count_safe_area(sensor_areas, y)
        ranges = remove_duplicated_ranges(ranges)
        if len(ranges) > 1:
            for p in zip(ranges[:-1], ranges[1:]):
                for x in range(p[0][1] + 1, p[1][0]):
                    if x >= 0 and x <= 4000000:
                        print((x, y), x * 4000000 + y)
            break