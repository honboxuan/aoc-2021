import argparse
import numpy as np
from numpy.core import multiarray
from scipy.signal import argrelextrema


def check(matrix, indices, index):
    if index not in indices:
        if matrix[index] < 9:
            indices.add(index)
            basin(matrix, indices, index)


def basin(matrix, indices, index):
    if index[0] > 0:
        left = (index[0] - 1, index[1])
        check(matrix, indices, left)
    if index[0] < matrix.shape[0] - 1:
        right = (index[0] + 1, index[1])
        check(matrix, indices, right)
    if index[1] > 0:
        top = (index[0], index[1] - 1)
        check(matrix, indices, top)
    if index[1] < matrix.shape[1] - 1:
        bottom = (index[0], index[1] + 1)
        check(matrix, indices, bottom)
    return len(indices)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    rows = []

    file = open(args["filepath"], "r")
    for line in file:
        row = list(map(int, line.strip()))
        rows.append(row)
    file.close()

    row_count = len(rows)
    col_count = len(rows[0])
    matrix = np.ndarray([row_count + 2, col_count + 2], dtype=int)
    matrix.fill(10)
    for i, row in enumerate(rows):
        matrix[i + 1, 1 : col_count + 1] = row

    # Part 1
    row_minima = argrelextrema(matrix, np.less, axis=0)
    row_minima = list(zip(row_minima[0], row_minima[1]))
    col_minima = argrelextrema(matrix, np.less, axis=1)
    col_minima = list(zip(col_minima[0], col_minima[1]))
    local_minima = []
    risk_sum = 0
    for index in row_minima:
        if index in col_minima:
            local_minima.append(index)
            risk_sum += matrix[index] + 1

    print("Part 1: ", risk_sum)

    # Part 2
    sizes = []
    for index in local_minima:
        indices = set()
        size = basin(
            matrix[1 : row_count + 1, 1 : col_count + 1],
            indices,
            (index[0] - 1, index[1] - 1),
        )
        sizes.append(size)
    sizes = sorted(sizes, reverse=True)

    print("Part 2: ", np.prod(sizes[:3]))
