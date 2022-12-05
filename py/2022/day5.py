import utils


def parse_input(path):
    allstr = utils.readall(path)
    [statstr, inststr] = allstr.split("\n\n")

    statlines = statstr.split("\n")
    idxline = statlines[-1]
    statlines = statlines[:-1]

    n = int(len(idxline) / 4) + 1

    status = [[] for i in range(n)]

    for l in statlines:
        for i in range(n):
            charpos = (i * 4) + 1
            if l[charpos] != ' ':
                status[i].append(l[charpos])

    inststr = inststr.replace("move ", "")
    inststr = inststr.replace(" from ", ",")
    inststr = inststr.replace(" to ", ",")
    instlines = inststr.split("\n")

    # Convert to 0 based index
    inst = [[int(l[0]), int(l[1]) - 1, int(l[2]) - 1]
            for l in [l.split(',') for l in instlines]]

    return (status, inst)


def print_status(stat):
    for i in range(len(stat)):
        print(f"{i}: {','.join(stat[i])}")


def move_n(status, f, t, n, reverse):
    temp = status[f][:n]
    if reverse:
        temp.reverse()

    status[f] = status[f][n:]
    temp.extend(status[t])
    status[t] = temp


def part1(path):
    (status, inst) = parse_input(path)

    for [n, f, t] in inst:
        move_n(status, f, t, n, True)

    print_status(status)
    print("".join([l[0] for l in status if l]))


def part2(path):
    (status, inst) = parse_input(path)

    for [n, f, t] in inst:
        move_n(status, f, t, n, False)

    print_status(status)
    print("".join([l[0] for l in status if l]))