import utils
import re
from functools import cache
from collections import deque
import itertools

data = []
valve_idx = None
path_map = None
dist_map = None


def parse_input(path):
    lines = utils.read_lines(path)

    matches = [
        re.match(
            r"Valve (..) has flow rate=([0-9]*); tunnels? leads? to valves? (.*)",
            l) for l in lines
    ]
    t = [(m.group(1), int(m.group(2)), m.group(3).split(", "))
         for m in matches]

    global valve_idx
    valve_idx = dict([(v[0], i) for i, v in enumerate(t)])

    return t


@cache
def best_path(closed, remain, pos):
    global data, valve_idx, path_map, dist_map

    if remain <= 1:
        return 0, []
    if len(closed) == 0:
        return 0, []

    new_closed = closed
    new_flow = 0
    if pos in closed:
        new_closed = tuple(x for x in closed if x != pos)
        remain -= 1
        new_flow = remain * data[pos][1]

    candidates = [(i, dist_map[pos][i]) for i in new_closed if data[i][1] > 0]
    paths = [best_path(new_closed, remain - d, i) for i, d in candidates]

    if len(paths) == 0:
        return new_flow, [pos]

    paths.sort(key=lambda x: -x[0])

    return new_flow + paths[0][0], [pos] + paths[0][1]


def shortest_path(data, valve_idx, i, j):
    queue = deque([(i, [])])
    visited = set([i])
    nvalve = len(data)

    while len(queue) > 0 and len(visited) < nvalve:
        cur, path = queue.popleft()
        if cur == j:
            return path

        connected = [
            valve_idx[vn] for vn in data[cur][2]
            if valve_idx[vn] not in visited
        ]
        queue.extend([(i, path + [i]) for i in connected])
        visited.add(cur)


def build_map(data, valve_idx):
    path_map = {}
    dist_map = {}
    for i, j in itertools.product(range(len(data)), range(len(data))):
        if i not in path_map:
            path_map[i] = {}
        if i not in dist_map:
            dist_map[i] = {}

        path_map[i][j] = shortest_path(data, valve_idx, i, j)
        dist_map[i][j] = len(path_map[i][j])

    return path_map, dist_map


def part1(path):
    global data, valve_idx, path_map, dist_map
    data = parse_input(path)
    nvalve = len(data)

    closed = tuple([i for i in range(nvalve) if data[i][1] > 0])
    path_map, dist_map = build_map(data, valve_idx)
    remain = 30

    result = best_path(closed, remain, valve_idx["AA"])

    print(result)


def part2(path):
    global data, valve_idx, path_map, dist_map
    data = parse_input(path)
    nvalve = len(data)

    closed = set([i for i in range(nvalve) if data[i][1] > 0])
    path_map, dist_map = build_map(data, valve_idx)
    remain = 26

    possible_combinations = []
    for i in range(len(closed)//2):
        possible_combinations.extend(itertools.combinations(closed, i+1))


    all_results = []
    start_idx = valve_idx["AA"]
    for c in possible_combinations:
        my_valves = c
        e_valves = tuple([i for i in closed if i not in c])

        if len(my_valves) == 0 or len(e_valves) == 0:
            print(my_valves, e_valves)
            return

        my_result = best_path(my_valves, remain, start_idx)
        e_result = best_path(e_valves, remain, start_idx)

        all_results.append((my_result[0] + e_result[0], my_result[1], e_result[1]))

    all_results.sort(key=lambda x: -x[0])

    print(all_results[0])
