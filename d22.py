import argparse
import numpy as np
import re


REGEXP = re.compile(
    r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
)


def clamp(v, low, high):
    return max(low, min(high, v))


def overlap(a1, a2, b1, b2):
    if a2 < b1 or b2 < a1:
        return 0
    return (max(a1, b1), min(a2, b2))


def unoverlapped(blocks):
    x = blocks[0][0:2]
    y = blocks[0][2:4]
    z = blocks[0][4:6]
    count = (abs(x[1] - x[0]) + 1) * (abs(y[1] - y[0]) + 1) * (abs(z[1] - z[0]) + 1)
    if len(blocks) == 1:
        return count

    overlaps = []
    for b in blocks[1:]:
        ox = overlap(x[0], x[1], b[0], b[1])
        oy = overlap(y[0], y[1], b[2], b[3])
        oz = overlap(z[0], z[1], b[4], b[5])
        if ox != 0 and oy != 0 and oz != 0:
            overlaps.append((ox[0], ox[1], oy[0], oy[1], oz[0], oz[1], b[6]))

    for i in range(len(overlaps)):
        count -= unoverlapped(overlaps[i:])
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    # Part 1

    reactor = np.ndarray([101, 101, 101], dtype=bool)
    reactor.fill(False)

    file = open(args["filepath"], "r")
    for line in file:
        match = REGEXP.search(line)
        if match:
            x1 = clamp(int(match[2]), -51, 51) + 50
            x2 = clamp(int(match[3]), -51, 51) + 50
            y1 = clamp(int(match[4]), -51, 51) + 50
            y2 = clamp(int(match[5]), -51, 51) + 50
            z1 = clamp(int(match[6]), -51, 51) + 50
            z2 = clamp(int(match[7]), -51, 51) + 50
            value = match[1] == "on"
            reactor[x1 : x2 + 1, y1 : y2 + 1, z1 : z2 + 1].fill(value)
    file.close()

    print("Part 1: ", np.count_nonzero(reactor))

    # Part 2

    blocks = []

    file = open(args["filepath"], "r")
    for line in file:
        match = REGEXP.search(line)
        if match:
            x1 = int(match[2])
            x2 = int(match[3])
            y1 = int(match[4])
            y2 = int(match[5])
            z1 = int(match[6])
            z2 = int(match[7])
            value = match[1] == "on"
            blocks.append((x1, x2, y1, y2, z1, z2, value))
    file.close()

    total = 0
    for i in range(len(blocks)):
        if blocks[i][6]:
            total += unoverlapped(blocks[i:])

    print("Part 2: ", total)
