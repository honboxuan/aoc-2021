import argparse
import numpy as np
import re

REGEXP = re.compile(r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)..(-?\d+)")


def dist_x(velocity, steps):
    vel_end = max(0, velocity - (steps - 1))
    steps = 1 + velocity - vel_end
    return int(steps * (velocity + vel_end) / 2)


def step_y(position, velocity):
    position += velocity
    velocity -= 1
    return (position, velocity)


def step(position, velocity):
    position += velocity
    velocity[0] += np.sign(velocity[0]) * -1
    velocity[1] -= 1
    return (position, velocity)


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
    line = file.readline().strip()
    file.close()

    match = REGEXP.search(line)
    x_min = int(match[1])
    x_max = int(match[2])
    y_min = int(match[3])
    y_max = int(match[4])

    # Assuming target is always to the bottom-right

    candidates = []
    vel_y = y_min
    while True:
        position = 0
        position_max = 0
        velocity = vel_y
        step_count = 0
        intersected = False
        while True:
            position, velocity = step_y(position, velocity)
            position_max = max(position_max, position)
            step_count += 1
            if position >= y_min and position <= y_max:
                intersected = True
                candidates.append((vel_y, step_count, position_max, position))
            elif position < y_min:
                break
        if intersected or vel_y < -y_min:
            vel_y += 1
        else:
            break

    # Part 1

    for candidate in reversed(candidates):
        # Try to calculate x velocity given number of steps
        steps = candidate[1]
        vel_x = 0
        intersected = False
        while True:
            position = dist_x(vel_x, steps)
            if position >= x_min and position <= x_max:
                intersected = True
                # Highest y found
                print("Part 1: ", candidate[2])
                # print(f"Initial velocity: ({vel_x}, {candidate[0]})")
                # print(f"Final position: ({position}, {candidate[3]})")
                break
            elif position > x_max:
                break
            vel_x += 1
        if intersected:
            break

    # Part 2

    valid = set()
    for candidate in candidates:
        steps = candidate[1]
        vel_x = 0
        while True:
            position = dist_x(vel_x, steps)
            if position >= x_min and position <= x_max:
                valid.add((vel_x, candidate[0]))
            elif position > x_max:
                break
            vel_x += 1

    print("Part 2: ", len(valid))
