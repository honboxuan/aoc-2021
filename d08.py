import argparse


def diff(a, b):
    return "".join(set(a).difference(set(b)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    signals = []
    outputs = []
    file = open(args["filepath"], "r")
    for line in file:
        sig, out = line.split(" | ")
        signals.append(sig.strip())
        outputs.append(out.strip())
    file.close()

    # Part 1
    occurences = 0
    for output in outputs:
        lengths = list(map(len, output.split(" ")))
        occurences += lengths.count(2)  # 1
        occurences += lengths.count(4)  # 4
        occurences += lengths.count(3)  # 7
        occurences += lengths.count(7)  # 8

    print("Part 1: ", occurences)

    # Part 2
    total = 0
    for i, signal in enumerate(signals):
        mapping = [""] * 10

        digits = list(map(lambda x: "".join(sorted(x)), signal.split(" ")))
        for digit in digits:
            length = len(digit)
            if length == 2:
                # 1
                mapping[1] = digit
            elif length == 3:
                # 7
                mapping[7] = digit
            elif length == 4:
                # 4
                mapping[4] = digit
            elif length == 5:
                # 2, 3, 5
                pass
            elif length == 6:
                # 0, 6, 9
                pass
            elif length == 7:
                # 8
                mapping[8] = digit

        # 1, 4, 7, 8 are known

        # a
        a = diff(mapping[7], mapping[1])
        bd = diff(mapping[4], mapping[1])
        eg = diff(diff(mapping[8], mapping[4]), a)

        # 0 has b but not d
        b = ""
        d = ""
        for digit in digits:
            if len(digit) == 6:
                d_candidate = diff(bd, digit)
                if len(d_candidate) == 1:
                    mapping[0] = digit
                    d = d_candidate
                    b = diff(bd, d)
                    break

        # 0, 1, 4, 7, 8 are known
        # a, b, d are known

        # 6 does not have c
        c = ""
        f = ""
        for digit in digits:
            if len(digit) == 6:
                c_candidate = diff(mapping[1], digit)
                if len(c_candidate) == 1:
                    mapping[6] = digit
                    c = c_candidate
                    f = diff(mapping[1], c)
                    break

        # 0, 1, 4, 6, 7, 8 are known
        # a, b, c, d, f are known
        e = ""
        g = ""
        for digit in digits:
            if len(digit) == 6:
                if digit not in mapping:
                    mapping[9] = digit
                    e = diff(mapping[6], mapping[9])
                    g = diff(eg, e)
                    break

        # 0, 1, 4, 6, 7, 8, 9 are known
        # a, b, c, d, e, f, g are known
        # Missing: 2, 3, 5
        mapping[2] = "".join(sorted([a, c, d, e, g]))
        mapping[3] = "".join(sorted([a, c, d, f, g]))
        mapping[5] = "".join(sorted([a, b, d, f, g]))

        mapping_inv = {v: i for i, v in enumerate(mapping)}
        digits_out = list(map(lambda x: "".join(sorted(x)), outputs[i].split(" ")))
        value = 0
        for digit in digits_out:
            value = 10 * value + mapping_inv[digit]
        total += value

    print("Part 2: ", total)
