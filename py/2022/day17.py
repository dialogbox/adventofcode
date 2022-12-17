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
    o[-1, :] = "-"
    o[-1, (0, -1)] = "+"

    print("=  CAVE =")
    for l in ["".join(l) for l in o]:
        print(l)


def part1(path):
    data = parse_input(path)

    cave = np.full((1, 9), fill_value=True)

    empty_space = np.full((7, 9), fill_value=False)
    empty_space[:, 0] = True
    empty_space[:, -1] = True

    i = 0
    for n in range(2022):
        # for n in range(11):
        block = blocks[n % 5]
        hwm = highest(cave)

        if hwm < 7:
            cave = np.vstack((np.full((7 - hwm, 9), fill_value=False), cave))
            cave[:7, :] = empty_space

        x, y = 3, 3

        while True:
            if data[i] == '<' and not conflict(cave, block, (x - 1, y)):
                x -= 1
            if data[i] == '>' and not conflict(cave, block, (x + 1, y)):
                x += 1

            i += 1
            if len(data) == i:
                print(f"overflow {n}")
                i = 0

            if conflict(cave, block, (x, y + 1)):
                mark_block(cave, block, (x, y), True)
                break

            y += 1

    print(len(cave) - highest(cave) - 1)


def part2(path):
    data = parse_input(path)

    print(len(data))