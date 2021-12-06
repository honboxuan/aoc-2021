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

    file = open(args["filepath"], "r")
    values = list(map(int, file.readline().split(",")))
    file.close()

    school = {}
    for value in values:
        if value not in school:
            school[value] = 0
        school[value] += 1

    # Part 1
    for i in range(80):
        school_tmp = {}
        for key, value in school.items():
            if key == 0:
                if 6 not in school_tmp:
                    school_tmp[6] = 0
                school_tmp[6] += value
                school_tmp[8] = value
            else:
                if key - 1 not in school_tmp:
                    school_tmp[key - 1] = 0
                school_tmp[key - 1] += value
        school = school_tmp
    total = 0
    for value in school.values():
        total += value

    print("Part 1: ", total)

    # Part 2
    for i in range(256 - 80):
        school_tmp = {}
        for key, value in school.items():
            if key == 0:
                if 6 not in school_tmp:
                    school_tmp[6] = 0
                school_tmp[6] += value
                school_tmp[8] = value
            else:
                if key - 1 not in school_tmp:
                    school_tmp[key - 1] = 0
                school_tmp[key - 1] += value
        school = school_tmp
    total = 0
    for value in school.values():
        total += value

    print("Part 2: ", total)
