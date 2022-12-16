import utils
from utils import Coord, Range
import itertools


def parse_input(path):
    lines = utils.read_lines(path)

    lines = [
        l.replace("Sensor at ",
                  "").replace(" closest beacon is at ",
                              "").replace(" ", "").replace("x=", "").replace(
                                  "y=", "").split(":") for l in lines
    ]
    sensors = [(Coord(l[0]), Coord(l[1])) for l in lines]

    return sensors


def mdist(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def yrange(s, b):
    mdist = abs(s.x - b.x) + abs(s.y - b.y)
    return Range(s.y - mdist, s.y + mdist)


def covered_ranges(sensors, y):
    matching_sensors = [(s, d) for s, (r, d) in sensors.items()
                        if r.is_included(y)]

    xranges = sorted([
        Range(s.x - (d - abs(y - s.y)), s.x + (d - abs(y - s.y)))
        for (s, d) in matching_sensors
    ])

    if len(xranges) == 0:
        return []

    result = []
    cur = xranges[0]
    for r in xranges[1:]:
        merged = cur.merge(r)
        if len(merged) > 1:
            result.append(merged[0])
            cur = merged[1]
        else:
            cur = merged[0]

    result.append(cur)

    return result


def part1test(path):
    input_data = parse_input(path)
    sensors = dict([(s, (yrange(s, b), mdist(s, b))) for (s, b) in input_data])
    beacons = set([b for (_, b) in input_data])

    ranges = covered_ranges(sensors, 10)
    num_beacons = 0
    for b in [b for b in beacons if b.y == 10]:
        for r in ranges:
            if r.is_included(b.x):
                num_beacons += 1

    print(sum([len(r) for r in ranges]) - num_beacons)


def part1(path):
    input_data = parse_input(path)
    sensors = dict([(s, (yrange(s, b), mdist(s, b))) for (s, b) in input_data])
    beacons = set([b for (_, b) in input_data])

    ranges = covered_ranges(sensors, 2000000)
    num_beacons = 0
    for b in [b for b in beacons if b.y == 2000000]:
        for r in ranges:
            if r.is_included(b.x):
                num_beacons += 1

    print(sum([len(r) for r in ranges]) - num_beacons)


def part2(path):
    input_data = parse_input(path)
    sensors = dict([(s, (yrange(s, b), mdist(s, b))) for (s, b) in input_data])

    for y in range(4000000):
        ranges = covered_ranges(sensors, y)
        if len(ranges) > 1:
            for (p1, p2) in zip(ranges[:-1], ranges[1:]):
                for x in range(p1.To + 1, p2.From):
                    if x >= 0 and x <= 4000000:
                        print((x, y), x * 4000000 + y)
            break


def part2new(path):
    input_data = parse_input(path)
    sensors = [(s, mdist(s, b)) for (s, b) in input_data]

    pairs = [((s1, d1), (s2, d2))
             for ((s1, d1), (s2, d2)) in itertools.combinations(sensors, 2)
             if mdist(s1, s2) == d1 + d2 + 2]

    if len(pairs) != 2:
        print("Something wrong!")
        return

    eq = []
    for ((s1, d1), (s2, d2)) in pairs:
        points1 = [
            Coord(s1.x - d1 - 1, s1.y),
            Coord(s1.x + d1 + 1, s1.y),
            Coord(s1.x, s1.y - d1 - 1),
            Coord(s1.x, s1.y + d1 + 1),
        ]
        [(_, p1), (_, p2)] = sorted([(mdist(s2, p), p) for p in points1])[:2]
        slope = (p2.y - p1.y) // (p2.x - p1.x)
        b = p1.y - slope * p1.x
        eq.append((-slope, b))

    # solve simultaneous equations
    # ax + by + p, cx + dy = q
    # y = (aq - cp) / (ad - bc), x = (dp - bq) / (ad - bc)
    [(a, p), (c, q)] = eq
    y = (a * q - c * p) // (a - c)
    x = (p - q) // (a - c)

    print((x, y), x * 4000000 + y)