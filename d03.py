import argparse
import numpy as np


def sum_bits(values, bit_position):
    sum = 0
    for value in values:
        if (1 << bit_position) & value:
            sum += 1
    return sum


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
    bit_count = 0
    values = []
    file = open(args["filepath"], "r")
    for line in file:
        if bit_count == 0:
            bit_count = len(line.strip())
        values.append(int(line, 2))
    file.close()

    bit_sums = [0] * bit_count
    for value in values:
        for i in range(bit_count):
            if (1 << i) & value:
                bit_sums[bit_count - 1 - i] += 1

    gamma = int("".join(map(str, 1 * (np.array(bit_sums) > len(values) / 2))), 2)
    epsilon = int("".join(map(str, 1 * (np.array(bit_sums) < len(values) / 2))), 2)

    print("Part 1: ", gamma * epsilon)

    # Part 2
    values_oxygen = values.copy()
    for i in range(bit_count):
        bit_position = bit_count - 1 - i
        sum = sum_bits(values_oxygen, bit_position)
        if sum >= len(values_oxygen) / 2:
            values_oxygen = [v for v in values_oxygen if ((1 << bit_position) & v)]
        else:
            values_oxygen = [v for v in values_oxygen if not ((1 << bit_position) & v)]
        if len(values_oxygen) == 1:
            break
    oxygen = values_oxygen[0]

    values_co2 = values.copy()
    for i in range(bit_count):
        bit_position = bit_count - 1 - i
        sum = sum_bits(values_co2, bit_position)
        if sum >= len(values_co2) / 2:
            values_co2 = [v for v in values_co2 if not ((1 << bit_position) & v)]
        else:
            values_co2 = [v for v in values_co2 if ((1 << bit_position) & v)]
        if len(values_co2) == 1:
            break
    co2 = values_co2[0]

    print("Part 2: ", oxygen * co2)
