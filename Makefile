# SPDX-FileCopyrightText: 2021 Uri Shaked
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

TARGETS = gds/skullfet_inverter.gds gds/skullfet_inverter.lef gds/skullfet_inverter_10x.gds gds/skullfet_inverter_10x.lef gds/skullfet_nand.gds gds/skullfet_nand.lef gds/skullfet_logo.gds gds/skullfet_logo.lef
SPICE_FILES = skullfet_inverter.spice skullfet_nand.spice
SPICE_INTERMEDIATE = $(SPICE_FILES:.spice=.sim) $(SPICE_FILES:.spice=.nodes) $(SPICE_FILES:.spice=.ext) $(SPICE_FILES:.spice=.res.ext)

all: gds $(TARGETS)
clean: 
	rm -f $(TARGETS) $(SPICE_FILES) $(SPICE_INTERMEDIATE)

.PHONY: all clean

magic_%: skullfet_%.mag
	magic -rcfile $(PDK_ROOT)/sky130A/libs.tech/magic/sky130A.magicrc $<

gds:
	mkdir gds

gds/skullfet_%.gds: skullfet_%.mag
	echo "gds write \"$@\"" | magic -rcfile $(PDK_ROOT)/sky130A/libs.tech/magic/sky130A.magicrc -noconsole -dnull $<

gds/skullfet_%.lef: skullfet_%.mag
	echo "lef write \"$@\" -pinonly" | magic -rcfile $(PDK_ROOT)/sky130A/libs.tech/magic/sky130A.magicrc -noconsole -dnull $<

skullfet_%.spice: skullfet_%.mag
	cat scripts/extract.tcl | magic -rcfile $(PDK_ROOT)/sky130A/libs.tech/magic/sky130A.magicrc -noconsole -dnull $<

spice: $(SPICE_FILES)
.PHONY: spice

sim_nand: skullfet_nand.spice
	echo ".lib '$(PDK_ROOT)/sky130A/libs.tech/ngspice/sky130.lib.spice' tt" > pdk_lib.spice
	ngspice sim_nand.spice
.PHONY: sim_nand
