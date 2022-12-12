from __future__ import annotations
import utils
import numpy as np
from collections import deque
from dataclasses import dataclass


@dataclass
class Point:
    coord: tuple[int, int]
    parent: Point = None

    def get_path(self: Point):
        cur = self
        result = []

        while cur != None:
            result.append(cur.coord)
            cur = cur.parent

        result.reverse()
        return result


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


def find_path_bfs(grid, startpos, endpos):
    queue = deque([Point(startpos)])
    visited = np.full(grid.shape, fill_value=False)
    visited[startpos] = True

    while len(queue) > 0:
        cur = queue.popleft()
        if cur.coord == endpos:
            return cur

        (y, x) = cur.coord

        for (ny, nx) in [(y, x - 1), (y, x + 1), (y - 1, x), (y + 1, x)]:
            if nx >= 0 and nx <= WIDTH - 1 and ny >= 0 and ny <= HEIGHT - 1:
                if not visited[ny, nx] and grid[ny, nx] <= grid[y, x] + 1:
                    queue.append(Point((ny, nx), cur))
                    visited[ny, nx] = True

    return False


def part1(path):
    grid = parse_input(path)

    end_points = find_path_bfs(grid, STARTPOS, ENDPOS)

    print(len(end_points.get_path()) - 1)


def part2(path):
    grid = parse_input(path)

    zeros = np.where(grid == 0)
    startposs = list(zip(zeros[0], zeros[1]))

    end_points = [find_path_bfs(grid, s, ENDPOS) for s in startposs]
    steps = sorted([len(t.get_path()) for t in end_points if t])

    print(steps[0] - 1)
