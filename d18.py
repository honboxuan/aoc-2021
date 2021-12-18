import argparse
import copy
import json
from itertools import permutations
from math import floor, ceil

LEFT = 1
RIGHT = 2


class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.depth = 0
        self.depth_inc()

    def is_leaf(self):
        return isinstance(self.left, int) and isinstance(self.right, int)

    def add_left(self, value):
        if isinstance(self.left, int):
            self.left += value
        else:
            self.left.add_left(value)

    def add_right(self, value):
        if isinstance(self.right, int):
            self.right += value
        else:
            self.right.add_right(value)

    def explode(self):
        if self.depth == 4:
            if isinstance(self.left, Node):
                # Explode left
                if isinstance(self.right, int):
                    self.right += self.left.right
                else:
                    self.right.add_left(self.left.right)
                value = self.left.left
                self.left = 0
                return LEFT, value

            if isinstance(self.right, Node):
                # Explode right
                if isinstance(self.left, int):
                    self.left += self.right.left
                else:
                    self.left.add_right(self.right.left)
                value = self.right.right
                self.right = 0
                return RIGHT, value
        else:
            if isinstance(self.left, Node):
                result = self.left.explode()
                if isinstance(result, bool):
                    if result is True:
                        return True
                else:
                    side, value = result
                    if side == RIGHT:
                        if isinstance(self.right, int):
                            self.right += value
                        else:
                            self.right.add_left(value)
                        return True
                    else:
                        return (side, value)

            if isinstance(self.right, Node):
                result = self.right.explode()
                if isinstance(result, bool):
                    if result is True:
                        return True
                else:
                    side, value = result
                    if side == LEFT:
                        if isinstance(self.left, int):
                            self.left += value
                        else:
                            self.left.add_right(value)
                        return True
                    else:
                        return (side, value)
        return False

    def split(self):
        if isinstance(self.left, int):
            if self.left >= 10:
                # Split left
                self.left = Node(floor(self.left / 2), ceil(self.left / 2))
                self.left.depth = self.depth + 1
                return True
        else:
            result = self.left.split()
            if result is True:
                return True

        if isinstance(self.right, int):
            if self.right >= 10:
                # Split right
                self.right = Node(floor(self.right / 2), ceil(self.right / 2))
                self.right.depth = self.depth + 1
                return True
        else:
            result = self.right.split()
            if result is True:
                return True

        return False

    def reduce(self):
        result = self.explode()
        if result is not False:
            return True
        return self.split()

    def depth_inc(self):
        self.depth += 1
        if isinstance(self.left, Node):
            self.left.depth_inc()
        if isinstance(self.right, Node):
            self.right.depth_inc()

    def depth_dec(self):
        self.depth -= 1
        if isinstance(self.left, Node):
            self.left.depth_dec()
        if isinstance(self.right, Node):
            self.right.depth_dec()

    def magnitude(self):
        if isinstance(self.left, int):
            left = self.left
        else:
            left = self.left.magnitude()
        if isinstance(self.right, int):
            right = self.right
        else:
            right = self.right.magnitude()
        return 3 * left + 2 * right

    def __str__(self):
        if isinstance(self.left, int):
            left = self.left
        else:
            left = str(self.left)
        if isinstance(self.right, int):
            right = self.right
        else:
            right = str(self.right)
        return f"[{left},{right}]"


def make_node(values):
    if isinstance(values, int):
        return values
    return Node(make_node(values[0]), make_node(values[1]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    nodes = []

    file = open(args["filepath"], "r")
    for line in file:
        values = json.loads(line)
        nodes.append(make_node(values))
    file.close()

    # Part 1

    nodes_p1 = copy.deepcopy(nodes)
    root = nodes_p1[0]
    for node in nodes_p1[1:]:
        root = Node(root, node)
        while True:
            result = root.reduce()
            if result is False:
                break

    print("Part 1: ", root.magnitude())

    # Part 2

    perm = list(permutations(range(len(nodes)), 2))
    magnitude_max = 0
    for i, j in perm:
        nodes_p2 = copy.deepcopy(nodes)
        root = Node(nodes_p2[i], nodes_p2[j])
        while True:
            result = root.reduce()
            if result is False:
                break

        magnitude = root.magnitude()
        if magnitude > magnitude_max:
            magnitude_max = magnitude

    print("Part 2: ", magnitude_max)
