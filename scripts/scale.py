# SPDX-FileCopyrightText: 2021 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("scale", type=int)
args = parser.parse_args()

scale = args.scale

# Pass 1: determine offset
lines = []
with open(args.file, "r") as inputfile:
    for line in inputfile:
        lines.append(line)

with open(args.file, "w") as outputfile:
    for line in lines:
        tokens = line.strip().split(" ")
        if tokens[0] == "rect":
            tokens[1] = str(int(tokens[1]) * scale)
            tokens[2] = str(int(tokens[2]) * scale)
            tokens[3] = str(int(tokens[3]) * scale)
            tokens[4] = str(int(tokens[4]) * scale)
            line = " ".join(tokens) + "\n"
        elif tokens[0] == "flabel":
            tokens[3] = str(int(tokens[3]) * scale)
            tokens[4] = str(int(tokens[4]) * scale)
            tokens[5] = str(int(tokens[5]) * scale)
            tokens[6] = str(int(tokens[6]) * scale)
            line = " ".join(tokens) + "\n"
        outputfile.write(line)
