#
# This is a legacy standalone script
# python3 dayXX.py
#
lines = [[[tuple(int(v) for v in l.split(',')),
           set()] for l in l[1:]] for l in [
               l.strip().split('\n')
               for l in open("inputs/day19.txt").read().split('\n\n')
           ]]


def distance(p1, p2):
    return sum([(p1[i] - p2[i])**2 for i in range(3)])**(1 / 2)


for scanner in lines:
    for probe in scanner:
        for probe2 in scanner:
            probe[1].add(distance(probe[0], probe2[0]))


def determinant(m):
    det = 0
    for i in range(3):
        det += (m[0][i] * (m[1][(i + 1) % 3] * m[2][(i + 2) % 3] -
                           m[1][(i + 2) % 3] * m[2][(i + 1) % 3]))
    return det


def inverse(m):
    det = determinant(m)
    return ((
        ((m[1][1] * m[2][2]) - (m[1][2] * m[2][1])) // det,
        (-((m[0][1] * m[2][2]) - (m[0][2] * m[2][1]))) // det,
        ((m[0][1] * m[1][2]) - (m[0][2] * m[1][1])) // det,
    ), (
        (-((m[1][0] * m[2][2]) - (m[1][2] * m[2][0]))) // det,
        ((m[0][0] * m[2][2]) - (m[0][2] * m[2][0])) // det,
        (-((m[0][0] * m[1][2]) - (m[0][2] * m[1][0]))) // det,
    ), (
        ((m[1][0] * m[2][1]) - (m[1][1] * m[2][0])) // det,
        (-((m[0][0] * m[2][1]) - (m[0][1] * m[2][0]))) // det,
        ((m[0][0] * m[1][1]) - (m[0][1] * m[1][0])) // det,
    ))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def minus(a):
    return (-a[0], -a[1], -a[2])


def apply_orientation(p, o):
    return (p[0] * o[0][0] + p[1] * o[0][1] + p[2] * o[0][2],
            p[0] * o[1][0] + p[1] * o[1][1] + p[2] * o[1][2],
            p[0] * o[2][0] + p[1] * o[2][1] + p[2] * o[2][2])


def triple(x):
    return ((x, 0, 0), (0, x, 0), (0, 0, x))


triples = [*triple(-1), *triple(1)]

orientations = [(x, y, z) for x in triples for y in triples for z in triples
                if determinant((x, y, z)) == 1]

beaconmap = {}
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        for beacon1 in lines[i]:
            for beacon2 in lines[j]:
                com = len(beacon1[1] & beacon2[1])
                if com >= 12:
                    beaconmap.setdefault((i, j), set()).add(
                        (beacon1[0], beacon2[0]))

transforms = {}
for b, vals in beaconmap.items():
    for o in orientations:
        s = set()
        for val in vals:
            s.add(distance(val[0], apply_orientation(val[1], o)))
        if len(s) == 1:
            A, B = val[0], apply_orientation(val[1], o)
            transforms[b] = [(add(A, minus(B)), o)]
            break

while len([*filter(lambda x: x[0] == 0, transforms)]) < len(lines) - 1:
    for b in range(len(lines)):
        for i in range(len(lines)):
            for j in range(len(lines)):
                if i == j or b == j:
                    continue
                if (rel1 := transforms.get(
                    (b, i))) and not (b, j) in transforms and (rel2 :=
                                                               transforms.get(
                                                                   (i, j))):
                    transforms[(b, j)] = [*rel2, *rel1]
                if (rel1 := transforms.get(
                    (b, i))) and not (b, j) in transforms and (rel2 :=
                                                               transforms.get(
                                                                   (j, i))):
                    transforms[(b, j)] = [
                        *[(apply_orientation(minus(v[0]), inv := inverse(
                            v[1])), inv)
                          for i, v in enumerate(reversed(rel2))], *rel1
                    ]

positions = {}
points = set()
for p in lines[0]:
    points.add(p[0])
for i in range(1, len(lines)):
    for p in lines[i]:
        testpoint = (0, 0, 0)
        point = p[0]
        for trans in transforms[(0, i)]:
            testpoint = add(trans[0], apply_orientation(testpoint, trans[1]))
            point = add(trans[0], apply_orientation(point, trans[1]))
        points.add(point)
    positions[i] = testpoint

print(
    len(points),
    max([
        sum(map(abs, add(i, minus(j)))) for i in positions.values()
        for j in positions.values()
    ]))
