import argparse
import collections
import numpy as np
from itertools import combinations


def rotate2d(coords, direction):
    return [direction * -1 * coords[1], direction * coords[0]]


def rotate(coords, axis, direction, turns):
    # Axis: x, y, z -> 0, 1, 2
    # Direction: -1 or 1
    # Each turn is 90 degrees
    tmp = list(coords)
    if axis == 0:
        for _ in range(turns):
            tmp[1:] = rotate2d(tmp[1:], direction)
    elif axis == 1:
        for _ in range(turns):
            tmp[0], tmp[2] = rotate2d([tmp[0], tmp[2]], direction)
    elif axis == 2:
        for _ in range(turns):
            tmp[:2] = rotate2d(tmp[:2], direction)
    return tuple(tmp)


def add(a, b):
    return tuple(np.array(a) + np.array(b))


def subtract(a, b):
    return tuple(np.array(a) - np.array(b))


def count_overlaps(ref, rotated_offset, offset):
    return len(ref.intersection(rotated_offset))


def compose(coords, a, d, t, turns):
    return rotate(rotate(coords, a, d, t), 2, 1, turns)


ADT = [
    (0, 1, 0),  # Up
    (0, 1, 1),  # Right
    (0, -1, 1),  # Left
    (0, 1, 2),  # Down
    (1, 1, 1),  # Front
    (1, -1, 1),  # Back
]


def align(ref, coords):
    for a, d, t in ADT:
        prerotated = set([rotate(c, a, d, t) for c in coords])
        for turns in range(4):
            rotated = set([rotate(c, 2, 1, turns) for c in prerotated])
            for r in ref:
                for c in rotated:
                    offset = subtract(r, c)
                    rotated_offset = set([add(v, offset) for v in rotated])
                    overlaps = count_overlaps(ref, rotated_offset, offset)
                    if overlaps >= 12:
                        ref = ref.union(rotated_offset)
                        # print("alignment: ", offset, axis, direction, turns)
                        return ref, True, offset, (a, d, t, turns)
    return ref, False, 0, ()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    scanners = []

    file = open(args["filepath"], "r")
    for line in file:
        line = line.strip()
        if "scanner" in line:
            scanners.append(set())
        else:
            if len(line) != 0:
                tokens = line.split(",")
                scanners[-1].add(tuple(map(int, tokens)))
    file.close()

    # Part 1

    failed = collections.defaultdict(lambda: {})

    offsets = np.ndarray([len(scanners), len(scanners)], dtype=tuple)
    rotations = np.ndarray([len(scanners), len(scanners)], dtype=tuple)

    unaligned = list(range(len(scanners)))
    while len(unaligned) > 1:
        print(unaligned)
        comb = combinations(unaligned, 2)
        i_prev = -1
        for i, j in comb:
            if i == i_prev or i not in unaligned or j not in unaligned:
                continue
            if j in failed[i]:
                continue
            print(
                f"Aligning {i} ({len(scanners[i])}) and {j} ({len(scanners[j])}): ",
                end="",
            )
            result, aligned, offset, rotation = align(scanners[i], scanners[j])
            if aligned:
                i_prev = i
                scanners[i] = result
                if i in failed:
                    del failed[i]
                if j in failed:
                    del failed[j]
                unaligned.remove(j)
                offsets[i, j] = offset
                rotations[i, j] = rotation
                print("Succeeded")
            else:
                failed[i][j] = True
                print("Failed")

    lengths = [len(scanner) for scanner in scanners]
    print("Part 1: ", max(lengths))

    file = open("beacons.txt", "w")
    file.write("\n".join(list(map(str, scanners[lengths.index(max(lengths))]))))
    file.close()

    # Part 2

    beacons = set()
    file = open("beacons.txt", "r")
    for line in file:
        line = line.strip()
        if len(line) != 0:
            beacons.add(tuple(eval(line)))
    file.close()

    scanner_locations = []

    for i, scanner in enumerate(scanners):
        print("Aligning ", i)
        result, aligned, offset, rotation = align(beacons, scanner)
        if aligned is False:
            print("Error")
        scanner_locations.append(offset)

    file = open("scanners.txt", "w")
    file.write("\n".join(list(map(str, scanner_locations))))
    file.close()

    scanner_positions = []
    file = open("scanners.txt", "r")
    for line in file:
        line = line.strip()
        if len(line) != 0:
            scanner_positions.append(tuple(eval(line)))
    file.close()

    offsets = np.ndarray([len(scanners), len(scanners)], dtype=tuple)
    offsets.fill((0, 0, 0))
    comb = combinations(range(len(scanners)), 2)
    for (i, j) in comb:
        if i != j:
            offsets[i, j] = subtract(scanner_positions[j], scanner_positions[i])

    distances = np.ndarray([len(scanners), len(scanners)], dtype=int)
    for index, value in np.ndenumerate(offsets):
        distances[index] = abs(value[0]) + abs(value[1]) + abs(value[2])

    print(distances)

    print("Part 2: ", np.max(distances))
