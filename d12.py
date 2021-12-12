import argparse


def traverse(nodes, paths, visited):
    for child in nodes[visited[-1]]:
        if child == "end":
            paths[0] += 1
        elif child.isupper() or child not in visited:
            traverse(nodes, paths, visited + [child])


def can_visit(node, visited):
    if node == "start":
        return False
    visited_lower = [node for node in visited if node.islower()]
    return (
        len(visited_lower) == len(set(visited_lower))
        or node.isupper()
        or node not in visited
    )


def traverse2(nodes, paths, visited):
    for child in nodes[visited[-1]]:
        if child == "end":
            paths[0] += 1
        else:
            if can_visit(child, visited):
                traverse2(nodes, paths, visited + [child])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    nodes = {}

    file = open(args["filepath"], "r")
    for line in file:
        tokens = line.strip().split("-")
        if tokens[0] not in nodes:
            nodes[tokens[0]] = set()
        nodes[tokens[0]].add(tokens[1])
        if tokens[1] not in nodes:
            nodes[tokens[1]] = set()
        nodes[tokens[1]].add(tokens[0])
    file.close()

    # Part 1
    paths = [0]
    visited = ["start"]
    traverse(nodes, paths, visited)

    print("Part 1: ", paths[0])

    # Part 2
    paths = [0]
    visited = ["start"]
    traverse2(nodes, paths, visited)

    print("Part 2: ", paths[0])
