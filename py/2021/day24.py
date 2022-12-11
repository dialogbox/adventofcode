#
# This is a legacy standalone script
# python3 dayXX.py
#
lines = open("./inputs/day24.txt", "r").read().splitlines()
ops = [l.split() for l in lines]

per_digit_ops = [ops[i:i + 18] for i in range(0, len(ops), 18)]

# if __name__ == "__main__":
#    with open("./inputs/day24.txt") as fh:
#        data = fh.read()
#    print("Part1:", solve([9] * 14, data))
#    print("Part2:", solve([1] * 14, data))

op4 = []
op5 = []
op15 = []

for digit in per_digit_ops:
    op4.append(int(digit[4][2]))
    op5.append(int(digit[5][2]))
    op15.append(int(digit[15][2]))


def print_stack(s):
    result = []
    while s > 0:
        result.append(s % 26)
        s = int(s / 26)

    result.reverse()

    print(result)


def doit(number):
    model_number = [int(d) for d in list(str(number))]
    z = 0

    for i in range(14):
        w = model_number[i]
        if (z % 26 + op5[i]) != w:
            z = int(z / op4[i]) * 26 + w + op15[i]
        else:
            z = int(z / op4[i])
        print_stack(z)
        # print(z)


def find_max():
    model_number = [9] * 14
    z = 0
    for i in range(14):
        w = model_number[i]
        if (z % 26 + op5[i]) != w:
            z = int(z / op4[i]) * 26 + w + op15[i]
        else:
            z = int(z / op4[i])
        print_stack(z)
        # print(z)


doit(99911993949684)
doit(62911941716111)
