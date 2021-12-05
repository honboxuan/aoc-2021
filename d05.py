import argparse
import re

REGEXP = re.compile(r"(\d+),(\d+) -> (\d+),(\d+)")


class LineSegment:
    def __init__(self, description):
        match = REGEXP.search(description)
        if match:
            self.x1 = int(match.group(1))
            self.y1 = int(match.group(2))
            self.x2 = int(match.group(3))
            self.y2 = int(match.group(4))

            if self.x1 > self.x2:
                self.x1, self.x2 = self.x2, self.x1
                self.y1, self.y2 = self.y2, self.y1

            self.is_valid = True
        else:
            print(f"No match: {description}")
            self.is_valid = False

    def is_horz(self):
        if not self.is_valid:
            return False
        return self.y1 == self.y2

    def is_vert(self):
        if not self.is_valid:
            return False
        return self.x1 == self.x2

    def is_horz_vert(self):
        return self.is_horz() or self.is_vert()

    def __str__(self):
        return f"{self.x1},{self.y1} to {self.x2},{self.y2}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filepath",
        nargs="?",
        default="input.txt",
        type=str,
    )
    args = vars(parser.parse_args())

    line_segments = []

    file = open(args["filepath"], "r")
    for line in file:
        line_segment = LineSegment(line)
        if line_segment.is_valid:
            line_segments.append(line_segment)
    file.close()

    diagram = {}

    # Part 1
    for line in line_segments:
        if line.is_horz():
            y = line.y1
            for x in range(line.x1, line.x2 + 1):
                key = (x, y)
                if key not in diagram:
                    diagram[key] = 0
                diagram[key] += 1
        elif line.is_vert():
            x = line.x1
            if line.y1 > line.y2:
                y_step = -1
            else:
                y_step = 1
            for y in range(line.y1, line.y2 + 1 * y_step, y_step):
                key = (x, y)
                if key not in diagram:
                    diagram[key] = 0
                diagram[key] += 1
    overlaps = len([value for value in diagram.values() if value > 1])

    print("Part 1: ", overlaps)

    # Part 2
    for line in line_segments:
        if not line.is_horz_vert():
            step_count = line.x2 - line.x1
            if line.y1 > line.y2:
                y_step = -1
            else:
                y_step = 1
            for i in range(step_count + 1):
                key = (line.x1 + i, line.y1 + i * y_step)
                if key not in diagram:
                    diagram[key] = 0
                diagram[key] += 1
    overlaps = len([value for value in diagram.values() if value > 1])

    print("Part 2: ", overlaps)
