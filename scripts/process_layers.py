#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Uri Shaked
# SPDX-License-Identifier: Apache-2.0

"""
Process layer definitions for different semiconductor processes.
This module contains the layer numbers and datatypes for various
semiconductor processes supported by the SkullFET generator.
"""

# Layer definitions for different processes
PROCESS_LAYERS = {
    # SKY130A process layers
    "sky130": {
        "diff": {"layer": 65, "datatype": 20},
        "poly": {"layer": 66, "datatype": 20},
        "psd": {"layer": 94, "datatype": 20},
        "licon": {"layer": 67, "datatype": 20},
        "metal1": {"layer": 68, "datatype": 20},
        "metal2": {"layer": 69, "datatype": 20},
        "nwell": {"layer": 64, "datatype": 20},
    },
    # IHP SG13G2 process layers
    "sg13g2": {
        "diff": {"layer": 1, "datatype": 0},  # Active.drawing
        "poly": {"layer": 5, "datatype": 0},  # GatePoly.drawing
        "psd": {"layer": 14, "datatype": 0},  # pSD.drawing
        "licon": {"layer": 8, "datatype": 0},  # Metal1.drawing
        "metal1": {"layer": 10, "datatype": 0},  # Metal2.drawing
        "metal2": {"layer": 30, "datatype": 0},  # Metal3.drawing
        "nwell": {"layer": 31, "datatype": 0},  # NWell.drawing
    },
}


def get_process_layers(process="sg13g2"):
    if process not in PROCESS_LAYERS:
        print(f"Error: Process '{process}' not supported. Using sg13g2 as default.")
        process = "sg13g2"

    return PROCESS_LAYERS[process]


def list_supported_processes():
    return list(PROCESS_LAYERS.keys())
