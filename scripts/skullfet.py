#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

import numpy as np
import gdstk
import argparse
from skullshapes import skull, bones
from process_layers import get_process_layers, list_supported_processes

# Constants for transformations
unit = np.eye(3)
rotate90 = np.array([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
rotate180 = rotate90.dot(rotate90)
rotate270 = np.array([[0, -1, 0], [-1, 0, 0], [0, 0, 1]])
vflip = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])  # Scale with y=-1


def translate(x, y):
    """Create a translation matrix"""
    return np.array([[1, 0, x], [0, 1, y], [0, 0, 1]])


def scale(x, y=None):
    """Create a scaling matrix"""
    if y is None:
        y = x
    return np.array([[x, 0, 0], [0, y, 0], [0, 0, 1]])


def bounds(rects, pad=0):
    """Calculate the bounding box of a set of rectangles"""
    minx = None
    miny = None
    maxx = None
    maxy = None
    for [x1, y1, x2, y2] in rects:
        if minx is None:
            minx = x1
            maxx = x1
            miny = y1
            maxy = y1
        minx = min(x1, x2, minx)
        maxx = max(x1, x2, maxx)
        miny = min(y1, y2, miny)
        maxy = max(y1, y2, maxy)
    return [[minx - pad, miny - pad, maxx + pad, maxy + pad]]


def transform(point, matrix):
    """Transform a point using a transformation matrix"""
    [x, y] = point
    [x, y, _] = matrix.dot([x, y, 1])
    return [x, y]


def create_polygon_from_rect(rect, matrix=unit, layer=None):
    """Convert a rectangle to a gdstk polygon with transformation"""
    x1, y1, x2, y2 = rect
    x1, y1 = transform([x1, y1], matrix)
    x2, y2 = transform([x2, y2], matrix)
    minx = min(x1, x2)
    miny = min(y1, y2)
    maxx = max(x1, x2)
    maxy = max(y1, y2)

    # Create a rectangle polygon
    points = [(minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy)]

    polygon = gdstk.Polygon(points)
    if layer is not None:
        polygon.layer = layer["layer"]
        polygon.datatype = layer["datatype"]

    return polygon


def create_cell_with_layers(name, process="sg13g2", draw_4_mosfets=False):
    """Create a GDSII cell with the skull and bones on different layers"""
    cell = gdstk.Cell(name)

    # Get layer definitions for the selected process
    layers = get_process_layers(process)

    scale_factor = 0.25
    nwell_padding = 1 if draw_4_mosfets else 2

    # Draw the skulls
    for layer in ["diff", "metal1", "metal2"]:
        for rect in skull:
            cell.add(
                create_polygon_from_rect(
                    rect, scale(scale_factor).dot(vflip), layers[layer]
                )
            )

            cell.add(
                create_polygon_from_rect(
                    rect, scale(scale_factor).dot(translate(0, -54)), layers[layer]
                )
            )

            # Extra two skulls for 4-MOSFET cells
            if draw_4_mosfets:
                cell.add(
                    create_polygon_from_rect(
                        rect,
                        scale(scale_factor).dot(translate(-20, -39)).dot(rotate90),
                        layers[layer],
                    )
                )

                cell.add(
                    create_polygon_from_rect(
                        rect,
                        scale(scale_factor).dot(translate(45, -14)).dot(rotate270),
                        layers[layer],
                    )
                )

    # Draw the bones on the metal layers
    for layer in ["metal1", "metal2"]:
        for rect in bones:
            cell.add(
                create_polygon_from_rect(
                    rect, scale(scale_factor).dot(translate(0, -34)), layers[layer]
                )
            )

    # Nwell around the skulls
    for rect in bounds(skull, pad=nwell_padding):
        cell.add(
            create_polygon_from_rect(
                rect, scale(scale_factor).dot(translate(0, -54)), layers["nwell"]
            )
        )

    if draw_4_mosfets:
        for rect in bounds(skull, pad=nwell_padding):
            cell.add(
                create_polygon_from_rect(
                    rect,
                    scale(scale_factor).dot(translate(45, -14)).dot(rotate270),
                    layers["nwell"],
                )
            )

    return cell


def main():
    """Main function to create and save the GDS file"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate SkullFET GDS file")
    parser.add_argument(
        "-t",
        "--type",
        choices=["inverter", "nand"],
        default="inverter",
        help="Cell type: inverter (2-MOSFET) or nand (4-MOSFET)",
    )
    parser.add_argument(
        "-p",
        "--process",
        choices=list_supported_processes(),
        default="sg13g2",
        help=f'Target process: {", ".join(list_supported_processes())}',
    )
    parser.add_argument("-o", "--output", default=None, help="Output GDS file name")
    args = parser.parse_args()

    # Set four_mosfets flag based on type if not explicitly set
    cell_name = f"skullfet_{args.type}"

    # Set default output filename based on type if not specified
    if args.output is None:
        args.output = f"{cell_name}.gds"

    # Create a new library
    lib = gdstk.Library()

    # Create the main cell
    main_cell = create_cell_with_layers(cell_name, args.process, args.type == "nand")
    lib.add(main_cell)

    # Save the library to a GDS file
    lib.write_gds(args.output)
    print(
        f"GDS file '{args.output}' has been created successfully for process '{args.process}'."
    )


if __name__ == "__main__":
    main()
