#!/usr/bin/env python3
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

import copy
import sys
sys.path.insert(0, '../../shared/')
from Register import *

def create_app_register(aName, aSize, aIndex, aType, aClass, aBoot, aAltPhysReg=None):
    new_reg = Register(**{'name':aName, 'length':aSize, 'index':aIndex, 'type':aType, 'class':aClass, 'boot':aBoot})
    new_field = RegisterField(aName)

    if aAltPhysReg is not None:
        new_field.mPhysicalRegister = aAltPhysReg # Alternative physical register specified.
    else:
        new_field.mPhysicalRegister = aName

    new_bit_field = BitField(aSize, 0)
    new_field.mBitFields.append(new_bit_field)
    new_reg.addRegisterFieldInOrder(new_field)
    return new_reg

def create_quad_precision_app_register(aIndex):
    q_reg = Register(**{'name':"Q%d" % aIndex, 'length':128, 'index':aIndex, 'type':"FPR", 'class':"LargeRegister", 'boot':0})
    for i in range(0, 2):
        q_field = RegisterField("Q%d_%d" % (aIndex, i))
        q_field.mPhysicalRegister = "f%d_%d" % (aIndex, i)
        q_bfield = BitField(64, 0)
        q_field.mBitFields.append(q_bfield)
        q_reg.addRegisterFieldInOrder(q_field)

    return q_reg

def create_vector_app_register(aIndex):
    v_reg = Register(**{'name':"V%d" % aIndex, 'length':128, 'index':aIndex, 'type':"VECREG", 'class':"LargeRegister", 'boot':0x3000})
    for i in range(0, 2):
        v_field = RegisterField("V%d_%d" % (aIndex, i))
        v_field.mPhysicalRegister = "v%d_%d" % (aIndex, i)
        v_bfield = BitField(64, 0)
        v_field.mBitFields.append(v_bfield)
        v_reg.addRegisterFieldInOrder(v_field)

    return v_reg

def build_app_registers():

    app_register_doc = RegistersDocument("RISC-V Registers")

    # Add x1-x31 registers
    for i in range(1, 32):
        app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("x%d" % i, 64, i, "GPR"))
        app_register_doc.addRegister(create_app_register("x%d" % i, 64, i, "GPR", None, 0x1000))

    # Add zero register
    app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("zero", 64, 0, "GPR", "PhysicalRegisterRazwi", 0))
    app_register_doc.addRegister(create_app_register("x0", 64, 0, "ZR", "ReadOnlyZeroRegister", 0, "zero"))

    # Add PC register
    app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("PC", 64, 32, "PC"))
    app_register_doc.addRegister(create_app_register("PC", 64, 32, "PC", None, 0))

    # Add f0-f31 and S0-S31
    for i in range(0, 32):
        app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("f%d_0" % i, 64, i, "FPR", aSubIndex=0))
        app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("f%d_1" % i, 64, i, "FPR", aSubIndex=1))
        app_register_doc.addRegister(create_app_register("S%d" % i, 32, i, "FPR", None, 0, "f%d_0" % i))

    # Add D0-D31
    for i in range(0, 32):
        app_register_doc.addRegister(create_app_register("D%d" % i, 64, i, "FPR", None, 0x3000, "f%d_0" % i))
    # Add Q0-Q31
    for i in range(0, 32):
        app_register_doc.addRegister(create_quad_precision_app_register(i))

    # add vector registers V0-V31
    for i in range(0, 32):
        app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("v%d_0" % i, 64, i, "VECREG", aSubIndex=0))
        app_register_doc.addPhysicalRegister(PhysicalRegister.createPhysicalRegister("v%d_1" % i, 64, i, "VECREG", aSubIndex=1))
        app_register_doc.addRegister(create_vector_app_register(i))

    app_register_doc.writeXmlFile('output/app_registers.xml')

if __name__ == "__main__":
    build_app_registers()
