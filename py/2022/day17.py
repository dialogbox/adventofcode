import utils
import numpy as np

blocks_data = [[
    "0000",
    "0000",
    "0000",
    "1111",
], [
    "000",
    "010",
    "111",
    "010",
], [
    "000",
    "001",
    "001",
    "111",
], [
    "1",
    "1",
    "1",
    "1",
], [
    "00",
    "00",
    "11",
    "11",
]]

blocks = []

for bstr in blocks_data:
    b = [[bool(int(c)) for c in list(l)] for l in bstr]
    b = np.array(b)
    blocks.append(b)


def parse_input(path):
    jet = list(utils.readall(path))

    return jet


def highest(cave):
    return np.argmax(cave[:, 1:-1]) // 7


def mark_block(cave, block, pos, v):
    block_width = block.shape[1]
    cave[pos[1] - 3:pos[1] + 1, pos[0]:pos[0] + block_width][block] = v


def conflict(cave, block, pos):
    block_width = block.shape[1]
    return np.any(cave[pos[1] - 3:pos[1] + 1,
                       pos[0]:pos[0] + block_width][block])


def print_cave(cave):
    o = np.full(cave.shape, fill_value=".")
    o[cave] = "#"
    o[:, (0, -1)] = "|"
    # o[-1, :] = "-"
    # o[-1, (0, -1)] = "+"

    print("=  CAVE =")
    for l in ["".join(l) for l in o]:
        print(l)


def simulate(cave, stream_dir, n):
    empty_space = np.full((7, 9), fill_value=False)
    empty_space[:, 0] = True
    empty_space[:, -1] = True

    i = 0
    for n in range(n):
        block = blocks[n % 5]
        hwm = highest(cave)

        if hwm < 7:
            cave = np.vstack((np.full((7 - hwm, 9), fill_value=False), cave))
            cave[:7, :] = empty_space

        x, y = 3, 3

        while True:
            if stream_dir[i] == '<' and not conflict(cave, block, (x - 1, y)):
                x -= 1
            if stream_dir[i] == '>' and not conflict(cave, block, (x + 1, y)):
                x += 1

            i += 1
            if len(stream_dir) == i:
                i = 0

            if conflict(cave, block, (x, y + 1)):
                mark_block(cave, block, (x, y), True)
                break

            y += 1

    hwm = highest(cave)

    return cave[hwm:-1, :]


def height(cave):
    return len(cave) - highest(cave)


def find_pattern(cave, stream_dir):
    empty_space = np.full((7, 9), fill_value=False)
    empty_space[:, 0] = True
    empty_space[:, -1] = True

    first_n = None
    first_height = None
    second_n = None
    second_height = None

    i = 0
    n = 0
    while True:
        block = blocks[n % 5]
        hwm = highest(cave)

        if hwm < 7:
            cave = np.vstack((np.full((7 - hwm, 9), fill_value=False), cave))
            cave[:7, :] = empty_space

        x, y = 3, 3

        while True:
            if stream_dir[i] == '<' and not conflict(cave, block, (x - 1, y)):
                x -= 1
            if stream_dir[i] == '>' and not conflict(cave, block, (x + 1, y)):
                x += 1

            i += 1
            if len(stream_dir) == i:
                i = 0

            if conflict(cave, block, (x, y + 1)):
                mark_block(cave, block, (x, y), True)
                if i == 1:
                    if first_n == None:
                        first_n = n
                        first_height = height(cave[:-1])
                    elif second_n == None:
                        second_n = n
                        second_height = height(cave[:-1])
                        return (first_n, second_n - first_n, n % 5, second_height - first_height)
                break

            y += 1

        n += 1


def part1(path):
    data = parse_input(path)

    cave = np.full((1, 9), fill_value=True)

    cave = simulate(cave, data, 2022)

    print(len(cave))


def part2(path):
    data = parse_input(path)

    cave = np.full((1, 9), fill_value=True)

    n1, steps, block, height_unit = find_pattern(cave, data)

    nrepeat = (1000000000000 - n1) // steps + 1
    left = (1000000000000 - n1) % steps

    cave = np.full((1, 9), fill_value=True)
    cave = simulate(cave, data, n1 + left)

    left_height = (len(cave) - height_unit)

    print(left_height + nrepeat * height_unit)