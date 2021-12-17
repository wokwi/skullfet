# SPDX-FileCopyrightText: 2021 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

import numpy as np
from skullshapes import skull, bones

unit = np.eye(3)


def translate(x, y):
    return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])


def scale(x, y=None):
    if y == None:
        y = x
    return np.array([[x, 0, 0], [0, y, 0], [0, 0, 1]])


def bounds(rects, pad=0):
    minx = None
    miny = None
    maxx = None
    maxy = None
    for [x1, y1, x2, y2] in rects:
        if minx == None:
            minx = x1
            maxx = x1
            miny = y1
            maxy = y1
        minx = min(x1, x2, minx)
        maxx = max(x1, x2, maxx)
        miny = min(y1, y2, miny)
        maxy = max(y1, y2, maxy)
    return [[minx - pad, miny - pad, maxx + pad, maxy + pad]]


vflip = scale(1, -1)


def transform(point, matrix):
    [x, y] = point
    [x, y, _] = matrix.dot([x, y, 1])
    return [x, y]


def draw(rects, matrix=unit):
    for rect in rects:
        x1, y1, x2, y2 = rect
        x1, y1 = transform([x1, y1], matrix)
        x2, y2 = transform([x2, y2], matrix)
        minx = round(min(x1, x2))
        miny = round(min(y1, y2))
        maxx = round(max(x1, x2))
        maxy = round(max(y1, y2))
        print("rect {} {} {} {}".format(minx, miny, maxx, maxy))


print("magic")
print("tech sky130A")
print("timestamp 1638034600")
print("<< ndiff >>")
draw(skull, scale(27).dot(vflip))
print("<< metal1 >>")
draw(bones, scale(27).dot(translate(0, -34)))
print("<< nwell >>")
draw(bounds(skull, pad=2), scale(27).dot(translate(0, -54)))
print("<< pdiff >>")
draw(skull, scale(27).dot(translate(0, -54)))
print("<< end >>")
