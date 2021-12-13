import argparse
import re

REGEXP_FOLD = re.compile(r"(x|y)=(\d+)")


def mirror(index, fold):
    if fold[0] == 0:
        if fold[1] < index[0]:
            return (2 * fold[1] - index[0], index[1])
        else:
            return index
    else:
        if fold[1] < index[1]:
            return (index[0], 2 * fold[1] - index[1])
        else:
            return index


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    paper = {}
    folds = []

    file = open(args["filepath"], "r")
    for line in file:
        match = REGEXP_FOLD.search(line)
        if match:
            folds.append((ord(match[1]) - ord("x"), int(match[2])))
        elif len(line.strip()) > 0:
            tokens = list(map(int, line.strip().split(",")))
            paper[(tokens[0], tokens[1])] = True
    file.close()

    # Part 1
    fold = folds[0]
    folded = paper.copy()
    for key, value in paper.items():
        # Remove fold
        if fold[0] == 0:
            if fold[1] == key[1]:
                if key in folded:
                    del folded[key]
                continue
        else:
            if fold[1] == key[0]:
                if key in folded:
                    del folded[key]
                continue

        key_fold = mirror(key, fold)
        if key != key_fold:
            if key in folded:
                del folded[key]
            folded[key_fold] = True
    paper = folded.copy()

    print("Part 1: ", sum(folded.values()))

    # Part 2
    for fold in folds[1:]:
        for key, value in paper.items():
            # Remove fold
            if fold[0] == 0:
                if fold[1] == key[1]:
                    if key in folded:
                        del folded[key]
                    continue
            else:
                if fold[1] == key[0]:
                    if key in folded:
                        del folded[key]
                    continue

            key_fold = mirror(key, fold)
            if key != key_fold:
                if key in folded:
                    del folded[key]
                folded[key_fold] = True
        paper = folded.copy()

    print("Part 2: ")
    (x_max, y_max) = map(max, *folded.keys())
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            key = (x, y)
            if key in folded:
                print("#", end="")
            else:
                print(".", end="")
        print("")
