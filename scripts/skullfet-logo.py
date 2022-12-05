# SPDX-FileCopyrightText: 2021 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

from os import path

grid = 10

# open the file in read mode from current directory/skullfet-logo.txt:
logo = open(path.join(path.dirname(path.realpath(__file__)), "skullfet-logo.txt"), "r").read()

def rect(x1, y1, x2, y2):
    minx = round(min(x1, x2))
    miny = round(min(y1, y2))
    maxx = round(max(x1, x2))
    maxy = round(max(y1, y2))
    return("rect {} {} {} {}".format(minx, miny, maxx, maxy))

print("magic")
print("tech sky130A")
print("timestamp 1638034600")

print("<< metal1 >>")
for y, line in enumerate(logo.splitlines()):
    for x, char in enumerate(line):
        if char == "█":
            print(rect(x * grid, -(y * 2) * grid, (x + 1) * grid, -(y * 2 + 2) * grid))
        if char == "▀":
            print(rect(x * grid, -(y * 2) * grid, (x + 1) * grid, -(y * 2 + 1) * grid))
        if char == "▄":
            print(rect(x * grid, -(y * 2 + 1) * grid, (x + 1) * grid, -(y * 2 + 2) * grid))

print("<< end >>")
