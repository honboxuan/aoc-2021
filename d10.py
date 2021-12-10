import argparse
import numpy as np
import re

REGEXP = re.compile(r"(:?\(\)|\[\]|\{\}|\<\>)")
CLOSE = re.compile(r"(:?\)|\]|\}|\>)")
SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
SCORE_2 = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def remove_pairs(line):
    while True:
        match = REGEXP.search(line)
        if match:
            line = REGEXP.sub("", line)
        else:
            break
    return line


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
    uncorrupted = []
    points = 0
    file = open(args["filepath"], "r")
    for line in file:
        line = remove_pairs(line)
        matched = False
        for match in CLOSE.finditer(line):
            matched = True
            points += SCORE[match[0]]
            break
        if not matched:
            uncorrupted.append(line)
    file.close()

    print("Part 1: ", points)

    # Part 2
    pointses = []
    for line in uncorrupted:
        points = 0
        for char in reversed(line.strip()):
            points = points * 5 + SCORE_2[char]
        pointses.append(points)

    print("Part 2: ", int(np.median(pointses)))
