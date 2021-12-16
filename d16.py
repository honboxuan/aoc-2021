import argparse
import numpy as np


class Packet:
    def __init__(self):
        self.version = 0
        self.type_id = 0
        self.value = 0
        self.sub_packets = []


def parse(line):
    packet = Packet()

    packet.version = int(line[:3], 2)
    line = line[3:]
    packet.type_id = int(line[:3], 2)
    line = line[3:]

    if packet.type_id == 4:
        # Literal value
        while True:
            bits = line[:5]
            line = line[5:]
            packet.value <<= 4
            packet.value += int(bits[1:], 2)
            if bits[0] == "0":
                break
    else:
        # Operator
        length_type_id = int(line[0])
        line = line[1:]
        if length_type_id == 0:
            # Next 15 bits: Total length in bits
            length_bits = int(line[:15], 2)
            line = line[15:]
            sub_packet_bits = line[:length_bits]
            line = line[length_bits:]
            while len(sub_packet_bits):
                sub_packet, sub_packet_bits = parse(sub_packet_bits)
                packet.sub_packets.append(sub_packet)
        elif length_type_id == 1:
            # Next 11 bits: Number of sub-packets
            sub_packet_count = int(line[:11], 2)
            line = line[11:]
            for _ in range(sub_packet_count):
                sub_packet, line = parse(line)
                packet.sub_packets.append(sub_packet)

        values = [sub_packet.value for sub_packet in packet.sub_packets]
        if packet.type_id == 0:
            # Sum packet
            packet.value = sum(values)
        elif packet.type_id == 1:
            # Product packet
            if len(values) == 1:
                packet.value = values[0]
            else:
                packet.value = np.prod(values)
        elif packet.type_id == 2:
            # Minimum packet
            packet.value = min(values)
        elif packet.type_id == 3:
            # Maximum packet
            packet.value = max(values)
        elif packet.type_id == 5:
            # Greater than packet
            if values[0] > values[1]:
                packet.value = 1
            else:
                packet.value = 0
        elif packet.type_id == 6:
            # Less than packet
            if values[0] < values[1]:
                packet.value = 1
            else:
                packet.value = 0
        elif packet.type_id == 7:
            # Equal to packet
            if values[0] == values[1]:
                packet.value = 1
            else:
                packet.value = 0

    return packet, line


def version_sum(packet):
    return packet.version + sum(
        [version_sum(sub_packet) for sub_packet in packet.sub_packets]
    )


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

    # Hex to bin
    line = "".join(["{:04b}".format(int(char, 16)) for char in line])

    packet, _ = parse(line)

    # Part 1
    print("Part 1: ", version_sum(packet))

    # Part 2

    print("Part 2: ", packet.value)
