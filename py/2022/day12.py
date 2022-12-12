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
                STARTPOS = (x, y)
                result[y][x] = 0
            elif c == ord('E') - ord('a'):
                ENDPOS = (x, y)
                result[y][x] = ord('z') - ord('a')

    result = np.array(result)

    return result


def find_path_dijkstra(grid, startpos, endpos):
    print(f"From: {startpos}, To: {endpos}")
    dist_heap = [[0 if (x, y) == startpos else sys.maxsize, (x, y)]
                 for x in range(WIDTH) for y in range(HEIGHT)]

    nodes = dict(zip([n[1] for n in dist_heap], dist_heap))

    visited = set()
    path = []
    heapq.heapify(dist_heap)

    while len(dist_heap) > 0 and dist_heap[0][0] != sys.maxsize:
        [curdist, (x, y)] = dist_heap[0]
        path.append((x, y))
        if (x, y) == endpos:
            break

        for (nx, ny) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
            if nx >= 0 and nx <= WIDTH - 1 and ny >= 0 and ny <= HEIGHT - 1:
                if (nx, ny) not in visited and grid[ny, nx] <= grid[y, x] + 1:
                    if nodes[(nx, ny)][0] > curdist + 1:
                        nodes[(nx, ny)][0] = curdist + 1
        visited.add((x, y))
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
                startposs.append((x, y))

    print(f"Starting Positions: {startposs}")
    print(sorted([find_path_dijkstra(grid, s, ENDPOS) for s in startposs])[0])
