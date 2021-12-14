import argparse
from collections import Counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    template = ""
    rules = {}

    file = open(args["filepath"], "r")
    for line in file:
        if len(template) == 0:
            # template = list(line.strip())
            template = line.strip()
        else:
            tokens = line.strip().split(" -> ")
            if len(tokens) == 2:
                rules[tokens[0]] = tokens[1]
    file.close()

    # Part 1
    polymer = template
    for _ in range(10):
        polymer_new = polymer[0]
        for i in range(len(polymer) - 1):
            pair = polymer[i : i + 2]
            polymer_new += rules[pair] + pair[1]
        polymer = polymer_new

    letters = list(set(polymer))
    counts = [polymer.count(letter) for letter in letters]

    print("Part 1: ", max(counts) - min(counts))

    # Part 2
    count = Counter()
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        count[pair] += 1
    for _ in range(40):
        count_new = Counter()
        for pair in count.keys():
            count_new[pair[0] + rules[pair]] += count[pair]
            count_new[rules[pair] + pair[1]] += count[pair]
        count = count_new

    result = Counter()
    for pair, value in count.items():
        result[pair[1]] += value
    result[template[0]] += 1

    print("Part 2: ", max(result.values()) - min(result.values()))

    # Part 2
