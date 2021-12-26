# SPDX-FileCopyrightText: 2021 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file")
args = parser.parse_args()

# Pass 1: determine offset
lines = []
x_vals = []
y_vals = []
with open(args.file, "r") as inputfile:
  for line in inputfile:
      tokens = line.strip().split(" ")
      if tokens[0] == "rect":
          x_vals.append(int(tokens[1]))
          y_vals.append(int(tokens[2]))
          x_vals.append(int(tokens[3]))
          y_vals.append(int(tokens[4]))
      elif tokens[0] == "flabel":
          x_vals.append(int(tokens[3]))
          y_vals.append(int(tokens[4]))
          x_vals.append(int(tokens[5]))
          y_vals.append(int(tokens[6]))
      lines.append(line)

x_offset = min(x_vals)
y_offset = min(y_vals)
print(x_offset, y_offset)
with open(args.file, "w") as outputfile:
  for line in lines:
      tokens = line.strip().split(" ")
      if tokens[0] == "rect":
          tokens[1] = str(int(tokens[1]) - x_offset)
          tokens[2] = str(int(tokens[2]) - y_offset)
          tokens[3] = str(int(tokens[3]) - x_offset)
          tokens[4] = str(int(tokens[4]) - y_offset)
          line = " ".join(tokens) + "\n"
      elif tokens[0] == "flabel":
          tokens[3] = str(int(tokens[3]) - x_offset)
          tokens[4] = str(int(tokens[4]) - y_offset)
          tokens[5] = str(int(tokens[5]) - x_offset)
          tokens[6] = str(int(tokens[6]) - y_offset)
          line = " ".join(tokens) + "\n"
      outputfile.write(line)
