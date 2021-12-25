map = [list(l)
       for l in open("./inputs/day25.txt", "r").read().splitlines()]

width = len(map[0])
height = len(map)


def move_down(current):
    moves = []
    for y in range(height):
        for x in range(width):
            if current[y][x] != 'v':
                continue

            if current[(y+1) % height][x] == '.':
                moves.append((x, y))

    for (x, y) in moves:
        current[(y+1) % height][x] = 'v'
        current[y][x] = '.'

    return len(moves)


def move_left(current):
    moves = []
    for y in range(height):
        for x in range(width):
            if current[y][x] != '>':
                continue

            if current[y][(x+1) % width] == '.':
                moves.append((x, y))

    for (x, y) in moves:
        current[y][(x+1) % width] = '>'
        current[y][x] = '.'

    return len(moves)


def print_map(current):
    print("------------")
    print("\n".join(["".join(l) for l in current]))
    print("------------")


print_map(map)
steps = 0
while True:
    n = move_left(map)
    n += move_down(map)

    steps += 1

    if n == 0:
        break

print_map(map)
print(steps)
