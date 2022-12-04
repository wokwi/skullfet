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
dualgate_layer = 55
dualgate_pad = 1000
bbox = layout.top_cell().bbox()
dualgate_box = pya.Box(bbox.left - dualgate_pad, bbox.bottom - dualgate_pad, bbox.right + dualgate_pad, bbox.top + dualgate_pad)
layout.top_cell().shapes(layout.layer(dualgate_layer, 0)).insert(dualgate_box)

layout.write(outfile)
