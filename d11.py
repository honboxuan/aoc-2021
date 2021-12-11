import argparse
import numpy as np


def get_neighbours(index):
    for x in range(-1, 2):
        for y in range(-1, 2):
            if x == 0 and y == 0:
                continue
            neighbour = (index[0] + x, index[1] + y)
            if (
                neighbour[0] >= 0
                and neighbour[0] < 10
                and neighbour[1] >= 0
                and neighbour[1] < 10
            ):
                yield neighbour


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    grid = np.ndarray([10, 10], dtype=int)

    file = open(args["filepath"], "r")
    for i, line in enumerate(file):
        grid[i, :] = list(map(int, line.strip()))
    file.close()

    # Part 1
    flash_count = 0
    for _ in range(100):
        grid += 1
        while np.any(grid > 9):
            for index, value in np.ndenumerate(grid > 9):
                if value:
                    grid[index] = 0
                    for i in get_neighbours(index):
                        if grid[i] != 0:
                            grid[i] += 1
        flash_count += np.count_nonzero(grid == 0)

    print("Part 1: ", flash_count)

    # Part 2
    step_count = 100
    while True:
        step_count += 1
        grid += 1
        while np.any(grid > 9):
            for index, value in np.ndenumerate(grid > 9):
                if value:
                    grid[index] = 0
                    for i in get_neighbours(index):
                        if grid[i] != 0:
                            grid[i] += 1
        if np.all(grid == 0):
            break

    print("Part 2: ", step_count)
