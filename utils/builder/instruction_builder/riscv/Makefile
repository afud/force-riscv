#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
# FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
INSTR_BUILDER=./instruction_builder.py
GVIMDIFF=/usr/bin/gvimdiff
INSTALL_DIR=../../../../riscv/arch_data

.PHONY: all
all:
	@make make_dir
	@make instructions
	@make install
	@make clean

.PHONY: make_dir
make_dir:
	@mkdir -p output

.PHONY: instructions
instructions: main_instructions c_instructions v_instructions priv_instructions
	@echo 'Building Instructions: all'
	@$(INSTR_BUILDER)

.PHONY: main_instructions
main_instructions: $(INSTR_BUILDER) input/riscv_instructions_starter.xml
	@echo 'Building Instructions: main'
	@$(INSTR_BUILDER) --main

.PHONY: c_instructions
c_instructions: $(INSTR_BUILDER) input/c_instructions_starter.xml
	@echo 'Building Instructions: c-ext'
	@$(INSTR_BUILDER) --c-ext

.PHONY: v_instructions
v_instructions: $(INSTR_BUILDER) input/v_instructions_starter.xml
	@echo 'Building Instructions: v-ext'
	@$(INSTR_BUILDER) --v-ext

.PHONY: priv_instructions
priv_instructions: $(INSTR_BUILDER) input/priv_instructions_starter.xml
	@echo 'Building Instructions: priv'
	@$(INSTR_BUILDER) --priv

.PHONY: install
install:
	@echo 'Building Instructions: installing instruction files'
	@cp -f output/supported_riscv_instructions.xml $(INSTALL_DIR)/riscv_instructions.xml
	@cp -f output/supported_c_instructions.xml $(INSTALL_DIR)/c_instructions.xml
	@cp -f output/supported_v_instructions.xml $(INSTALL_DIR)/v_instructions.xml
	@cp -f output/supported_priv_instructions.xml $(INSTALL_DIR)/priv_instructions.xml

.PHONY: diff
diff:
	@$(GVIMDIFF) output/supported_riscv_instructions.xml $(INSTALL_DIR)/riscv_instructions.xml

.PHONY: clean
clean:
	@echo 'Building Instructions: clean'
	@rm -f output/*.xml output/*.txt
