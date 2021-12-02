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

    depth_values = []

    file = open(args["filepath"], "r")
    for line in file:
        depth_values.append(int(line))
    file.close()

    # Part 1
    print("Part 1: ", np.sum(np.diff(depth_values) > 0))

    # Part 2
    sums = np.convolve(depth_values, np.ones(3, dtype=int), "valid")
    print("Part 2: ", np.sum(np.diff(sums) > 0))
