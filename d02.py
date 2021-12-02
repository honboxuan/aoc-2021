import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    # Part 1
    horizontal = 0
    depth = 0
    file = open(args["filepath"], "r")
    for line in file:
        tokens = line.strip().split(" ")
        command = tokens[0]
        value = int(tokens[1])
        if command == "forward":
            horizontal += value
        elif command == "down":
            depth += value
        elif command == "up":
            depth -= value
    file.close()
    print("Part 1: ", horizontal * depth)

    # Part 2
    horizontal = 0
    depth = 0
    aim = 0
    file = open(args["filepath"], "r")
    for line in file:
        tokens = line.strip().split(" ")
        command = tokens[0]
        value = int(tokens[1])
        if command == "forward":
            horizontal += value
            depth += aim * value
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value
    file.close()
    print("Part 2: ", horizontal * depth)
