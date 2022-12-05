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

all: gds $(TARGETS)
clean: 
	rm -f $(TARGETS)

.PHONY: all clean

magic_%: skullfet_%.mag
	magic -rcfile $(PDK_ROOT)/gf180mcuC/libs.tech/magic/gf180mcuC.magicrc $<

gds:
	mkdir gds

gds/skullfet_%.gds: skullfet_%.mag
	echo "gds write \"$@__magic\"" | magic -rcfile $(PDK_ROOT)/gf180mcuC/libs.tech/magic/gf180mcuC.magicrc -noconsole -dnull $<
	klayout -b -r skullfet_gf180.py -rd "infile=$@__magic" -rd "outfile=$@"

gds/skullfet_%.lef: skullfet_%.mag
	echo "lef write \"$@\"" | magic -rcfile $(PDK_ROOT)/gf180mcuC/libs.tech/magic/gf180mcuC.magicrc -noconsole -dnull $<

extract:
	echo "extract\next2spice lvs\next2spice cthresh 0\next2spice" | magic -rcfile $(PDK_ROOT)/gf180mcuC/libs.tech/magic/gf180mcuC.magicrc -noconsole -dnull skullfet_inverter.mag
