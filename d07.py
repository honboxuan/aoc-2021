import argparse
import numpy as np

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
    positions = np.array(list(map(int, file.readline().split(","))))
    file.close()

    # Part 1
    cost = np.nan
    for i in range(min(positions), max(positions) + 1):
        tmp = np.sum(np.abs(positions - i))
        if np.isnan(cost) or tmp < cost:
            cost = tmp

    print("Part 1: ", cost)

    # Part 2
    cost = np.nan
    for i in range(min(positions), max(positions) + 1):
        tmp = np.abs(positions - i)
        tmp = np.multiply(tmp, (tmp + 1) / 2)
        tmp = np.sum(tmp)
        if np.isnan(cost) or tmp < cost:
            cost = tmp

    print("Part 2: ", int(cost))
