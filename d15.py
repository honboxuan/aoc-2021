import argparse
import numpy as np
from dijkstar import Graph, find_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    risks = []
    file = open(args["filepath"], "r")
    for line in file:
        risks.append(list(map(int, line.strip())))
    file.close()

    rows = len(risks)
    cols = len(risks[0])

    # Part 1
    graph = Graph()
    for i in range(rows):
        for j in range(cols):
            if i < rows - 1:
                graph.add_edge((i, j), (i + 1, j), risks[i + 1][j])
            if j < cols - 1:
                graph.add_edge((i, j), (i, j + 1), risks[i][j + 1])
    path = find_path(graph, (0, 0), (rows - 1, cols - 1))
    print("Part 1: ", path.total_cost)

    # Part 2
    risks = np.array(risks)
    risks_tiled = np.ndarray([5 * rows, 5 * cols], dtype=int)
    risks_tiled.fill(0)
    for i in range(5):
        for j in range(5):
            tile = risks + i + j
            for index, value in np.ndenumerate(tile):
                value %= 9
                if value == 0:
                    value = 9
                tile[index] = value
            row = i * rows
            col = j * cols
            risks_tiled[row : row + rows, col : col + cols] = tile

    graph = Graph()
    for index, risk in np.ndenumerate(risks_tiled):
        i = index[0]
        j = index[1]
        if i > 0:
            graph.add_edge((i, j), (i - 1, j), risks_tiled[i - 1, j])
        if i < risks_tiled.shape[0] - 1:
            graph.add_edge((i, j), (i + 1, j), risks_tiled[i + 1, j])
        if j > 0:
            graph.add_edge((i, j), (i, j - 1), risks_tiled[i, j - 1])
        if j < risks_tiled.shape[1] - 1:
            graph.add_edge((i, j), (i, j + 1), risks_tiled[i, j + 1])
    path = find_path(
        graph,
        (0, 0),
        (risks_tiled.shape[0] - 1, risks_tiled.shape[1] - 1),
    )
    print("Part 2: ", path.total_cost)
