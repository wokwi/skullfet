# Run this script with the following command:
# klayout -b -r skullfet_gf180.py -rd infile=filename.gds -rd outfile=filename_fixed.gds

import sys
import pya

# read input filename from command line
layout = pya.Layout()
layout.read(infile)

# set database unit to 0.005 micron
layout.dbu = 0.005

# Surround the design with a dualgate box:
dualgate_layer = layout.layer(55, 0)
dualgate_pad = 1000
dualgate_box = layout.top_cell().bbox().enlarged(pya.Point(dualgate_pad, dualgate_pad))
layout.top_cell().shapes(dualgate_layer).insert(dualgate_box)

# Add padding around COMP layer where NPLUS is present
comp_layer = layout.layer(22, 0)
nplus_layer = layout.layer(32, 0)
comp_padding = 140
it = layout.top_cell().begin_shapes_rec(comp_layer)
new_boxes = []
remove_boxes = []
while not it.at_end():
  for shape in layout.top_cell().shapes(nplus_layer).each_overlapping(it.shape().bbox()):
    if shape.is_box():
      remove_boxes.append(shape)
      nplus_box = shape.bbox().enlarged(pya.Point(comp_padding, comp_padding))
      new_boxes.append(nplus_box)
  it.next()
for box in remove_boxes:
  layout.top_cell().shapes(nplus_layer).erase(box)
for box in new_boxes:
  layout.top_cell().shapes(nplus_layer).insert(box)

layout.write(outfile)
