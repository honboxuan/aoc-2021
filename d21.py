import argparse
import re
from functools import cache

REGEXP = re.compile(r"Player (\d) starting position: (\d+)")


def inc_die(die):
    return (die % 100) + 1


def roll_die(die):
    sum = 0
    for _ in range(3):
        die = inc_die(die)
        sum += die
    return die, sum


@cache
def iterate(pos_1, pos_2, score_1, score_2, player):
    wins_1 = 0
    wins_2 = 0
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                if player == 1:
                    pos = (pos_1 + a + b + c - 1) % 10 + 1
                    score = score_1 + pos
                    if score >= 21:
                        wins_1 += 1
                    else:
                        w1, w2 = iterate(pos, pos_2, score, score_2, 2)
                        wins_1 += w1
                        wins_2 += w2
                else:
                    pos = (pos_2 + a + b + c - 1) % 10 + 1
                    score = score_2 + pos
                    if score >= 21:
                        wins_2 += 1
                    else:
                        w1, w2 = iterate(pos_1, pos, score_1, score, 1)
                        wins_1 += w1
                        wins_2 += w2
    return wins_1, wins_2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    pos_start = [0] * 2

    file = open(args["filepath"], "r")
    for line in file:
        match = REGEXP.search(line.strip())
        if match:
            pos_start[int(match[1]) - 1] = int(match[2])
    file.close()

    # Part 1

    pos = pos_start.copy()
    score = [0] * 2
    die = 0
    roll_count = 0
    score_loser = 0
    while True:
        term = False
        for i in range(2):
            die, move = roll_die(die)
            roll_count += 3
            pos[i] = (pos[i] - 1 + move) % 10 + 1
            score[i] += pos[i]
            # print(move, pos[i], score[i])
            if score[i] >= 1000:
                score_loser = score[i - 1]
                term = True
                break
        if term:
            break

    print("Part 1: ", score_loser * roll_count)

    # Part 2
    w1, w2 = iterate(pos_start[0], pos_start[1], 0, 0, 1)
    print("Part 2: ", max([w1, w2]))
