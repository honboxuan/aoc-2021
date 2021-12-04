import argparse
import numpy as np
import re


class Board:
    def __init__(self):
        self.numbers = np.ndarray([5, 5], dtype=int)
        self.marks = np.ndarray([5, 5], dtype=bool)
        self.marks.fill(False)
        self.index_line = 0

    def add_line(self, line):
        tokens = line.split(" ")
        for i, token in enumerate(tokens):
            self.numbers[self.index_line, i] = int(token)
        self.index_line += 1
        # if self.is_complete():
        #     print(self.__str__())

    def is_complete(self):
        return self.index_line == 5

    def __str__(self):
        return str(self.numbers)

    def mark(self, number):
        self.marks |= self.numbers == number
        # print(self.marks)

    def check(self):
        for i in range(5):
            row = self.marks[i, :]
            if row.all():
                return True
            col = self.marks[:, i]
            if col.all():
                return True
        return False

    def score(self):
        unmarked_sum = 0
        for i, marked in np.ndenumerate(self.marks):
            if not marked:
                unmarked_sum += self.numbers[i]
        return unmarked_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    chosen_values = []
    boards = [Board()]

    file = open(args["filepath"], "r")
    for line in file:
        line = re.sub(" +", " ", line.strip())
        if len(chosen_values) == 0:
            chosen_values = list(map(int, line.split(",")))
            # print(chosen_values)
        elif len(line) > 0:
            if boards[-1].is_complete():
                boards.append(Board())
            boards[-1].add_line(line)
    file.close()

    # Part 1
    winning_board = 0
    winning_value = np.nan
    for value in chosen_values:
        for board in boards:
            board.mark(value)
            if board.check():
                winning_board = board
                winning_value = value
                break
        if not np.isnan(winning_value):
            break

    print("Part 1: ", winning_board.score() * winning_value)

    # Part 2
    winning_board = 0
    winning_value = np.nan
    boards_bin = []
    for value in chosen_values:
        for board in boards:
            board.mark(value)
            if board.check():
                if len(boards) > 1:
                    boards_bin.append(board)
                else:
                    winning_board = board
                    winning_value = value
                    break

        if not np.isnan(winning_value):
            break

        for board in boards_bin:
            boards.remove(board)
        boards_bin = []

    print("Part 2: ", winning_board.score() * winning_value)
