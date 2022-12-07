from __future__ import annotations
import utils
from dataclasses import dataclass
import bisect


@dataclass
class Entry:
    name: str
    type: str
    subdir: dict
    parent: Entry
    size: int


def parse_input(path):
    root = Entry('/', 'd', {}, None, -1)
    cur = root

    inputstr = utils.readall(path)
    cmds = [c.strip().splitlines() for c in inputstr.split("$") if c]

    for cmd in cmds:
        argv = cmd[0].split(" ")
        result = cmd[1:]

        if argv[0] == "cd":
            dest_dir = argv[1]
            if dest_dir == "..":
                cur = cur.parent
            elif dest_dir == "/":
                cur = root
            else:
                cur = cur.subdir[dest_dir]
        elif argv[0] == "ls":
            for tl in result:
                tokens = tl.split(" ")
                if tokens[0] == "dir":
                    cur.subdir[tokens[1]] = Entry(tokens[1], 'd', {}, cur, -1)
                else:
                    cur.subdir[tokens[1]] = Entry(tokens[1], 'f', {}, cur,
                                                  int(tokens[0]))

    return root


def cal_total_sum_of_a_dir(dir: Entry):
    if dir.size != -1:
        return dir.size

    dir.size = sum([cal_total_sum_of_a_dir(dir.subdir[f]) for f in dir.subdir])
    return dir.size


def all_dir(dir: Entry, fullpath: str):
    if dir.type != "d":
        return []

    result = [(fullpath, dir.name, dir.size, dir)]

    for n in dir.subdir:
        result.extend(all_dir(dir.subdir[n], f"{fullpath}{n}/"))

    return result


def part1(path):
    root = parse_input(path)

    cal_total_sum_of_a_dir(root)
    l = all_dir(root, "/")

    print(sum([d[2] for d in l if d[2] < 100000]))


def part2(path):
    root = parse_input(path)

    cal_total_sum_of_a_dir(root)
    l = sorted(all_dir(root, "/"), key=lambda i: i[2])

    free_size = 70000000 - root.size
    require_size = 30000000 - free_size
    idx = bisect.bisect_left(l, require_size, key=lambda i: i[2])

    print(l[idx][2])