import heapq
import sys
import utils
import numpy as np
from functools import cache

HEIGHT = 0
WIDTH = 0
STARTPOS = (0, 0)
ENDPOS = (0, 0)


def parse_input(path):
    sourcemap = utils.read_grid(path)

    result = [[ord(c) - ord('a') for c in l] for l in sourcemap]

    global HEIGHT
    global WIDTH
    global STARTPOS
    global ENDPOS
    HEIGHT = len(result)
    WIDTH = len(result[0])

    for y, l in enumerate(result):
        for x, c in enumerate(l):
            if c == ord('S') - ord('a'):
                STARTPOS = (y, x)
                result[y][x] = 0
            elif c == ord('E') - ord('a'):
                ENDPOS = (y, x)
                result[y][x] = ord('z') - ord('a')

    result = np.array(result)

    return result


def find_path_dijkstra(grid, startpos, endpos):
    print(f"From: {startpos}, To: {endpos}")
    dist_heap = [[0 if (y, x) == startpos else sys.maxsize, (y, x)]
                 for x in range(WIDTH) for y in range(HEIGHT)]

    nodes = dict(zip([n[1] for n in dist_heap], dist_heap))

    visited = set()
    path = []
    heapq.heapify(dist_heap)

    while len(dist_heap) > 0 and dist_heap[0][0] != sys.maxsize:
        [curdist, (y, x)] = dist_heap[0]
        path.append((y, x))
        if (y, x) == endpos:
            break

        for (ny, nx) in [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]:
            if nx >= 0 and nx <= WIDTH - 1 and ny >= 0 and ny <= HEIGHT - 1:
                if (ny, nx) not in visited and grid[ny, nx] <= grid[y, x] + 1:
                    if nodes[(ny, nx)][0] > curdist + 1:
                        nodes[(ny, nx)][0] = curdist + 1
        visited.add((y, x))
        heapq.heappop(dist_heap)
        heapq.heapify(dist_heap)

    return nodes[endpos][0]


def part1(path):
    grid = parse_input(path)

    print(STARTPOS, ENDPOS)
    print(find_path_dijkstra(grid, STARTPOS, ENDPOS))


def part2(path):
    grid = parse_input(path)

    print(ENDPOS)

    startposs = []

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y, x] == 0:
                startposs.append((y, x))

    print(f"Starting Positions: {startposs}")
    print(sorted([find_path_dijkstra(grid, s, ENDPOS) for s in startposs])[0])
