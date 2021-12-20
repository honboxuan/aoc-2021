import argparse
import numpy as np


def get_neighbours(image, index, default):
    rows = len(image)
    cols = len(image[0])
    for r in range(index[0] - 1, index[0] + 2):
        for c in range(index[1] - 1, index[1] + 2):
            if r < 0 or r >= rows or c < 0 or c >= cols:
                yield default
                continue
            yield image[r][c]


def get_output(iea, image, index, default):
    value = 0
    for v in get_neighbours(image, index, default):
        value = value * 2 + v
    return iea[value]


def trim(image):
    while image[0].count(True) == 0:
        image = image[1:]
    while image[-1].count(True) == 0:
        image = image[:-1]
    tmp = np.array(image)
    while np.count_nonzero(tmp[:, 0]) == 0:
        tmp = tmp[:, 1:]
    while np.count_nonzero(tmp[:, -1]) == 0:
        tmp = tmp[:, :-1]
    return tmp.tolist()


def print_image(image):
    for row in image:
        for v in row:
            if v:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    file = open(args["filepath"], "r")
    line = file.readline().strip()
    iea = [c == "#" for c in line]

    image = []
    for line in file:
        line = line.strip()
        if len(line):
            image.append([c == "#" for c in line])
    file.close()

    # Part 1

    default = False
    for _ in range(2):
        output = []
        for r in range(-3, len(image) + 3):
            output.append([])
            for c in range(-3, len(image[0]) + 3):
                output[r + 3].append(get_output(iea, image, (r, c), default))
        default = output[0][0]
        image = trim(output)

    print("Part 1: ", np.count_nonzero(np.array(image)))

    # Part 2
    for _ in range(48):
        output = []
        for r in range(-3, len(image) + 3):
            output.append([])
            for c in range(-3, len(image[0]) + 3):
                output[r + 3].append(get_output(iea, image, (r, c), default))
        default = output[0][0]
        image = trim(output)

    print("Part 2: ", np.count_nonzero(np.array(image)))
