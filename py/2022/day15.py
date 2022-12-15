import utils
from utils import IntCoord, IntRange


def parse_input(path):
    lines = utils.read_lines(path)

    lines = [
        l.replace("Sensor at ",
                  "").replace(" closest beacon is at ",
                              "").replace(" ", "").replace("x=", "").replace(
                                  "y=", "").split(":") for l in lines
    ]
    sensors = [(IntCoord(l[0]), IntCoord(l[1])) for l in lines]

    return sensors


def mdist(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def yrange(s, b):
    mdist = abs(s.x - b.x) + abs(s.y - b.y)
    return IntRange(s.y - mdist, s.y + mdist)


def covered_ranges(sensors, y):
    matching_sensors = [(s, d) for s, (r, d) in sensors.items()
                        if r.is_included(y)]

    xranges = sorted([
        IntRange(s.x - (d - abs(y - s.y)), s.x + (d - abs(y - s.y)))
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