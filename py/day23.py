import time
from copy import deepcopy
from functools import cache

initial_status = [list(l[1:-1])
                  for l in open("./inputs/day23part2.txt", "r").read().splitlines()[1:-1]]

width = len(initial_status[0])

target_pos = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
energes = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}


def find_move_outs(status, start_loc):
    hallway = status[0]
    rooms = status[1:]
    possibilities = []

    if start_loc not in [2, 4, 6, 8]:
        return possibilities

    room = [rooms[i][start_loc] for i in range(len(rooms))]
    # if room is already empty
    if len(list(filter(lambda p: p != '.', room))) == 0:
        return possibilities

    vpos = [i for i in range(len(room)) if room[i] != '.'][0]
    kind = room[vpos]
    target = target_pos[kind]
    energe = energes[kind]

    # nothing need to move
    if len([p for p in room if p != '.' and target_pos[p] != start_loc]) == 0:
        return possibilities

    cur = start_loc
    steps = vpos + 1
    while cur > 0 and hallway[cur-1] == '.':
        cur -= 1
        steps += 1
        if cur not in [2, 4, 6, 8]:
            new_map = deepcopy(status)
            new_map[vpos+1][start_loc] = '.'
            new_map[0][cur] = kind

            possibilities.append(tuple([new_map, steps * energe]))

    cur = start_loc
    steps = vpos + 1
    while cur < width-1 and hallway[cur + 1] == '.':
        cur += 1
        steps += 1
        if cur not in [2, 4, 6, 8]:
            new_map = deepcopy(status)
            new_map[vpos+1][start_loc] = '.'
            new_map[0][cur] = kind

            possibilities.append(tuple([new_map, steps * energe]))

    return possibilities


def check_move_in(status, start_loc):
    hallway = status[0]
    rooms = status[1:]

    possibilities = []

    kind = hallway[start_loc]
    if kind == '.' or kind not in target_pos:
        return possibilities

    energe = energes[kind]
    target = target_pos[kind]

    room = [rooms[i][target] for i in range(len(rooms))]
    # if room is not empty or occupied by others
    if len(list(filter(lambda p: p != '.' and p != kind, room))) > 0:
        return possibilities

    vpos = len(room) - len([p for p in room if p != '.']) - 1

    steps = vpos + 1
    # check if the hallway toward to the dest is clear
    if start_loc > target:
        # move left
        if len(list(filter(lambda c: c != '.', hallway[target:start_loc]))) > 0:
            return []
        steps += start_loc - target
    else:
        # move right
        if len(list(filter(lambda c: c != '.', hallway[start_loc+1:target+1]))) > 0:
            return []
        steps += target - start_loc

    new_status = deepcopy(status)
    new_status[0][start_loc] = '.'
    new_status[vpos+1][target] = kind

    return [(new_status, steps * energe)]


def is_done(status):
    for i in range(1, len(status)):
        if (status[i][2] != 'A'
            or status[i][4] != 'B'
            or status[i][6] != 'C'
                or status[i][8] != 'D'):
            return False
    return True


@cache
def cheapest(status_str):
    # print(status_str)
    # time.sleep(0.1)

    status = [list(l) for l in status_str.splitlines()]
    min_energe = 9999999999999

    new_status = []
    for i in range(width):
        if i in [2, 4, 6, 8]:
            for m in find_move_outs(status, i):
                new_status.append(m)
        else:
            for m in check_move_in(status, i):
                new_status.append(m)

    for m in new_status:
        if is_done(m[0]):
            # print("Done from")
            # print(status_to_str(status))
            min_energe = min(min_energe, m[1])
        else:
            min_energe = min(
                min_energe, m[1] + cheapest("\n".join(["".join(l) for l in m[0]])))

    return min_energe


def status_to_str(status):
    for l in status:
        print("".join(l))


result = cheapest("\n".join(["".join(l) for l in initial_status]))
print(result)
