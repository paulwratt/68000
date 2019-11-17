#!/usr/bin/env python3
#
# Motorola 68000 Disassembler
# Copyright (c) 2019 by Jeff Tranter <tranter@pobox.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Disassembly format:
# AAAAAAAA  XX XX XX XX XX XX XX XX XX XX  MMMM.s  operands
# 00001000  4E 71                          NOP
# 00001002  60 FC                          BRA.s   $12345678
# 00001004  67 FA                          BEQ.s   $12345678
# 00001006  60 00 FF F8                    BRA.w   $12345678
# 0000107E  00 79 00 FF 00 00 12 34        ORI.w   #$FF,$1234
# 00001086  00 B9 00 00 00 FF 12 34 56 78  ORI.l   #$ff,$12345678
# 0000109E  4E F9 00 00 10 00              JMP     $DEADBEEF
#
# With --nolist option:
# MMMM.s  operands
# NOP
# BRA.s   $12345678
# BEQ.s   $12345678
# BRA.w   $12345678
# ORI.w   #$FF,$1234
# ORI.l   #$ff,$12345678
# JMP     $DEADBEEF

# To Do:
#
# - Implement all 68000 instructions and addressing modes
# - Stress test
# - Implement -n option
# - Test that output can be assembled
# - Move CSV file into table in code, remove unused fields
# - Refactor any common code into functions

import argparse
import csv
import re
import sys

# Data/Tables

conditions = ("T", "F", "HI", "LS", "CC", "CS", "NE", "EQ", "VC", "VS", "PL", "MI", "GE", "LT", "GT", "LE")

# Functions


# Print a disassembled line of output
def printInstruction(address, length, mnemonic, data, operand):
    if length == 2:
        line = "{0:08X}  {1:02X} {2:02X}                          {3:8s}  {4:s}".format(address,
                                                                                        data[0],
                                                                                        data[1],
                                                                                        mnemonic,
                                                                                        operand)
    elif length == 4:
        line = "{0:08X}  {1:02X} {2:02X} {3:02X} {4:02X}                    {5:8s}  {6:s}".format(address,
                                                                                                  data[0],
                                                                                                  data[1],
                                                                                                  data[2],
                                                                                                  data[3],
                                                                                                  mnemonic,
                                                                                                  operand)
    elif length == 6:
        line = "{0:08X}  {1:02X} {2:02X} {3:02X} {4:02X} {5:02X} {6:02X}              {7:8s}  {8:s}".format(address,
                                                                                                            data[0],
                                                                                                            data[1],
                                                                                                            data[2],
                                                                                                            data[3],
                                                                                                            data[4],
                                                                                                            data[5],
                                                                                                            mnemonic,
                                                                                                            operand)
    elif length == 8:
        line = "{0:08X}  {1:02X} {2:02X} {3:02X} {4:02X} {5:02X} {6:02X} {7:02X} {8:02X}        {9:8s}  {10:s}".format(address,
                                                                                                                       data[0],
                                                                                                                       data[1],
                                                                                                                       data[2],
                                                                                                                       data[3],
                                                                                                                       data[4],
                                                                                                                       data[5],
                                                                                                                       data[6],
                                                                                                                       data[7],
                                                                                                                       mnemonic,
                                                                                                                       operand)
    elif length == 10:
        line = "{0:08X}  {1:02X} {2:02X} {3:02X} {4:02X} {5:02X} {6:02X} {7:02X} {8:02X} {9:02X} {10:02X}  {11:8s}  {12:s}".format(address,
                                                                                                                                   data[0],
                                                                                                                                   data[1],
                                                                                                                                   data[2],
                                                                                                                                   data[3],
                                                                                                                                   data[4],
                                                                                                                                   data[5],
                                                                                                                                   data[6],
                                                                                                                                   data[7],
                                                                                                                                   data[8],
                                                                                                                                   data[9],
                                                                                                                                   mnemonic,
                                                                                                                                   operand)
    else:
        print("Error: Invalid length {0:d} passed to printInstruction().".format(length))
        sys.exit(1)

    print(line)


# Return a register list as used by the MOVEM instruction.
# Parameter mask has the 16-bit register mask.
# Parameter aFirst is set true if MSB is A7, otherwise is D0.
def registerList(aFirst, mask):
    if mask < 0 or mask > 0xffff:
        print("Error: bad mask {0:d} passed to registerList().".format(mask))
        sys.exit(1)

    result = ""
    first = True

    for bit in range(16):
        if mask & (1 << bit):
            if not first:
                result = result + "/"
            first = False
            if aFirst:
                if bit <= 7:
                    result = result + "A{0:d}".format(7 - bit)
                else:
                    result = result + "D{0:d}".format(15 - bit)
            else:
                if bit <= 7:
                    result = result + "D{0:d}".format(bit)
                else:
                    result = result + "A{0:d}".format(bit - 8)

    return result


# Caalculate and return string for effective address.
# Given M and Xn bits.
# Parameter s should be the character "b", "w", or "l".
# Also uses global variables data and length.
def EffectiveAddress(s, m, xn):
    if m == 0:  # Dn
        operand = "D{0:n}".format(xn)
    elif m == 1:  # An
        operand = "A{0:n}".format(xn)
    elif m == 2:  # (An)
        operand = "(A{0:n})".format(xn)
    elif m == 3:  # (An)+
        operand = "(A{0:n})+".format(xn)
    elif m == 4:  # -(An)
        operand = "-(A{0:n})".format(xn)
    elif m == 5:  # d16(An)
        operand = "${0:02X}{1:02X}(A{2:n})".format(data[length-2], data[length-1], xn)
    elif m == 6:  # d8(An,Xn)
        if data[length-2] & 0x80:
            operand = "${0:02X}(A{1:n},A{2:n})".format(data[length-1], xn, (data[length-2] & 0x70) >> 4)
        else:
            operand = "${0:02X}(A{1:n},D{2:n})".format(data[length-1], xn, (data[length-2] & 0x70) >> 4)
    elif m == 7 and xn == 0:  # abs.W
        operand = "${0:02X}{1:02X}".format(data[length-2], data[length-1])
    elif m == 7 and xn == 1:  # abs.L
        operand = "${0:02X}{1:02X}{2:02X}{3:02X}".format(data[length-4], data[length-3], data[length-2], data[length-1])
    elif m == 7 and xn == 2:  # d16(PC)
        operand = "${0:02X}{1:02X}(PC)".format(data[length-2], data[length-1])
    elif m == 7 and xn == 3:  # d8(PC,Xn)
        if data[length-2] & 0x80:
            operand = "${0:02X}(PC,A{1:d})".format(data[length-1], (data[length-2] & 0x70) >> 4)
        else:
            operand = "${0:02X}(PC,D{1:d})".format(data[length-1], (data[length-2] & 0x70) >> 4)
    elif m == 7 and xn == 4:  # #imm
        if s == "b" or s == "w":
            operand = "#${0:02X}{1:02X}".format(data[length-2], data[length-1])
        elif s == "l":
            operand = "#${0:02X}{1:02X}{2:02X}{3:02X}".format(data[length-4], data[length-3], data[length-2], data[length-1])
        else:
            print("Error: Invalid S value passed to EffectiveAddress().")
            operand = ""
    else:
        print("Error: Invalid addressing mode passed to EffectiveAddress(),", s, m, xn)
        operand = ""

    return operand


# Return instruction length based on S bits, type 1
def SLength1(s):
    if s == 0:
        return "b"
    elif s == 1:
        return "w"
    elif s == 2:
        return "l"
    else:
        print("Error: Invalid S bits.")
        return "w"


# Return instruction length based on S bits, type 2
def SLength2(s):
    if s == 1:
        return "b"
    elif s == 3:
        return "w"
    elif s == 2:
        return "l"
    else:
        print("Error: Invalid S bits.")
        return "w"


# Return instruction length based on S bits, type 3
def SLength3(s):
    if s == 0:
        return "w"
    elif s == 1:
        return "l"
    else:
        print("Error: Invalid S bit.")
        return "w"


# Return length of standard instruction based on S, M, and Xn bits
# Parameter s should be the character "b", "w", or "l".
def InstructionLength(s, m, xn):
    if m == 0:  # Dn
        return 2
    elif m == 1:  # An
        return 2
    elif m == 2:  # (An)
        return 2
    elif m == 3:  # (An)+
        return 2
    elif m == 4:  # -(An)
        return 2
    elif m == 5:  # d16(An)
        return 4
    elif m == 6:  # d8(An,Xn)
        return 4
    elif m == 7 and xn == 0:  # abs.W
        return 4
    elif m == 7 and xn == 1:  # abs.L
        return 6
    elif m == 7 and xn == 2:  # d16(PC)
        return 4
    elif m == 7 and xn == 3:  # d8(PC,Xn)
        return 4
    elif m == 7 and xn == 4:  # #imm
        if s == "b":
            return 4
        elif s == "w":
            return 4
        elif s == "l":
            return 6
        else:
            print("Invalid s value passed to InstructionLength().")
            return 6
    else:
        print("Error: Invalid addressing mode passed to InstructionLength(),", s, m, xn)
        return 2


# Initialize variables
address = 0            # Start address if instruction
length = 0             # Length of instruction in bytes
mnemonic = ""          # Mnemonic string
sourceAddressMode = 0  # Addressing mode for source operand
destAddressMode = 0    # Addressing mode for destination operand
data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Instruction bytes

# Parse command line options
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Binary file to disassemble")
parser.add_argument("-n", "--nolist", help="Don't list instruction bytes (make output suitable for assembler)", action="store_true")
parser.add_argument("-a", "--address", help="Specify decimal starting address (defaults to 0)", default=0, type=int)
args = parser.parse_args()
address = args.address

# Address must be even
if address % 2:
    print("Error: Start address must be even.")
    sys.exit(1)

# Open CSV file of opcodes and read into table
with open("opcodetable.csv", newline='') as csvfile:
    table = list(csv.DictReader(csvfile))

    # Do validity check on table entries and calculate bitmask and value
    # for each opcode so we can quicky test opcode for matches in the
    # table.

    for row in table:

        # Validity check: Mnemonic is not empty.
        if row["Mnemonic"] == "":
            print("Error: Empty mnemonic entry in opcode table:", row)
            sys.exit(1)

        # Validity check: B W and L are empty or the corresponding letter
        if not row["B"] in ("B", ""):
            print("Error: Bad B entry in opcode table:", row)
            sys.exit(1)
        if not row["W"] in ("W", ""):
            print("Error: Bad W entry in opcode table:", row)
            sys.exit(1)
        if not row["L"] in ("L", ""):
            print("Error: Bad L entry in opcode table:", row)
            sys.exit(1)

        # Pattern  has length 16 and each character is 0, 1, or X.
        if not re.match(r"^[01X]...............$", row["Pattern"]):
            print("Error: Bad pattern entry in opcode table:", row)
            sys.exit(1)

        # Validity check: DataSize is B, W, L, A, or empty.
        if not row["DataSize"] in ("B", "W", "L", "A", ""):
            print("Error: Bad DataSize entry in opcode table:", row)
            sys.exit(1)

        # Validity check: DataType is is I, N, D, M or empty.
        if not row["DataType"] in ("I", "N", "D", "M", ""):
            print("Error: Bad DataType entry in opcode table:", row)
            sys.exit(1)

        # Convert bit pattern to 16-bit value and bitmask, e.g.
        # pattern: 1101XXX110001XXX
        #   value: 1101000110001000
        #    mask: 1111000111111000
        # Opcode matches pattern if opcode AND mask equals value

        pattern = row["Pattern"]
        value = ""
        mask = ""

        for pos in range(16):
            if pattern[pos] in ("0", "1"):
                value += pattern[pos]
                mask += "1"
            else:
                value += "0"
                mask += "0"

        # Convert value and mask to numbers and store in table.
        row["Value"] = int(value, 2)
        row["Mask"] = int(mask, 2)

# Open input file
filename = args.filename
try:
    f = open(filename, "rb")
except FileNotFoundError:
    print(("Error: input file '{}' not found.".format(filename)), file=sys.stderr)
    sys.exit(1)

# Loop over file input
while True:

    # Get 16-bit instruction
    c1 = f.read(1)  # Get binary bytes from file
    if len(c1) == 0:  # handle EOF
        break
    c2 = f.read(1)
    if len(c2) == 0:
        break

    data[0] = ord(c1)  # Convert to numbers
    data[1] = ord(c2)

    # Get op code
    opcode = data[0]*256 + data[1]

    # Find matching mnemonic in table
    for row in table:
        value = row["Value"]
        mask = row["Mask"]
        mnemonic = row["Mnemonic"]

        if (opcode & mask) == value:
            break

    # Should now have the mnemonic
    if mnemonic == "":
        print("Error: Mnemonic not found in opcode table.")
        sys.exit(1)

    # Handle instruction types - one word implicit with no operands:
    # ILLEGAL, RESET, NOP, RTE, RTS, TRAPV, RTR, UNIMPLEMENTED, INVALID
    if mnemonic in ("ILLEGAL", "RESET", "NOP", "RTE", "RTS", "TRAPV", "RTR", "UNIMPLEMENTED", "INVALID"):
        length = 2
        printInstruction(address, length, mnemonic, data, "")

    # Handle instruction types - one word implicit with operands
    # TRAP
    elif mnemonic == "TRAP":
        length = 2
        operand = "#${0:02X}".format(data[1] & 0x0f)
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: ORI to CCR
    elif mnemonic in ("ORI to CCR", "EORI to CCR"):
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        if data[2] != 0:
            print("Warning: MSB of operand should be zero, but is {0:02X}".format(data[2]))
        operand = "#${0:02X},CCR".format(data[3])
        if mnemonic == "ORI to CCR":
            printInstruction(address, length, "ORI", data, operand)
        else:
            printInstruction(address, length, "EORI", data, operand)

    # Handle instruction types: ORI to SR
    elif mnemonic in ("ORI to SR", "EORI to SR"):
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        operand = "#${0:02X}{1:02X},SR".format(data[2], data[3])
        if mnemonic == "ORI to SR":
            printInstruction(address, length, "ORI", data, operand)
        else:
            printInstruction(address, length, "EORI", data, operand)

    # Handle instruction types: ANDI to CCR
    elif mnemonic == "ANDI to CCR":
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        if data[2] != 0:
            print("Warning: MSB of operand should be zero, but is {0:02X}".format(data[2]))
        operand = "#${0:02X},CCR".format(data[3])
        printInstruction(address, length, "ANDI", data, operand)

    # Handle instruction types: ANDI to SR
    elif mnemonic == "ANDI to SR":
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        operand = "#${0:02X}{1:02X},SR".format(data[2], data[3])
        printInstruction(address, length, "ANDI", data, operand)

    # Handle instruction types: STOP
    elif mnemonic == "STOP":
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        operand = "#${0:02X}{1:02X}".format(data[2], data[3])
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types - BRA, BSR, Bcc
    elif mnemonic in ("BRA", "BSR", "BCC"):
        if (data[1]) != 0:  # Byte offset
            length = 2
            disp = data[1]
            if disp < 128:  # Positive offset
                dest = address + disp + 2
            else:  # Negative offset
                dest = address - (disp ^ 0xff) + 1
        else:  # Word offset
            length = 4
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            disp = data[2]*256 + data[3]
            if disp < 32768:  # Positive offset
                dest = address + disp + 2
            else:  # Negative offset
                dest = address - (disp ^ 0xffff) + 1
        operand = "${0:08X}".format(dest)

        if mnemonic == "BCC":
            cond = data[0] & 0x0f
            mnemonic = "B" + conditions[cond]

        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types - UNLK
    elif mnemonic == "UNLK":
        length = 2
        operand = "A{0:d}".format(data[1] & 0x07)
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types - LINK
    elif mnemonic == "LINK":
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        operand = "A{0:d},#${1:02X}{2:02X}".format(data[1] & 0x07, data[2], data[3])
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types - SWAP
    elif mnemonic == "SWAP":
        length = 2
        operand = "D{0:d}".format(data[1] & 0x07)
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types - EXT
    elif mnemonic == "EXT":
        length = 2
        operand = "D{0:d}".format(data[1] & 0x07)
        if data[1] & 0x40:
            printInstruction(address, length, "EXT.l", data, operand)
        else:
            printInstruction(address, length, "EXT.w", data, operand)

    # Handle instruction types - MOVE USP
    elif mnemonic == "MOVE USP":
        length = 2
        if data[1] & 0x08:
            operand = "USP,A{0:d}".format(data[1] & 0x07)
        else:
            operand = "A{0:d},USP".format(data[1] & 0x07)
        printInstruction(address, length, "MOVE", data, operand)

    elif mnemonic == "DBCC":
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        disp = data[2]*256 + data[3]
        if disp < 32768:  # Positive offset
            dest = address + disp + 2
        else:  # Negative offset
            dest = address - (disp ^ 0xffff) + 1
        operand = "D{0:d},${1:08X}".format(data[1] & 0x07, dest)

        cond = data[0] & 0x0f
        mnemonic = "DB" + conditions[cond]

        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "MOVEP":
        length = 4
        data[2] = ord(f.read(1))
        data[3] = ord(f.read(1))
        disp = data[2]*256 + data[3]
        op = (data[1] & 0xc0) >> 6
        if op == 0:
            mnemonic = "MOVEP.w"
            operand = "(${0:04X},A{1:d}),D{2:d}".format(disp, data[1] & 0x07, (data[0] & 0x0e) >> 1)
        elif op == 1:
            mnemonic = "MOVEP.l"
            operand = "(${0:04X},A{1:d}),D{2:d}".format(disp, data[1] & 0x07, (data[0] & 0x0e) >> 1)
        elif op == 2:
            mnemonic = "MOVEP.w"
            operand = "D{0:d},(${1:04X},A{2:d})".format((data[0] & 0x0e) >> 1, disp, data[1] & 0x07)
        elif op == 3:
            mnemonic = "MOVEP.l"
            operand = "D{0:d},(${1:04X},A{2:d})".format((data[0] & 0x0e) >> 1, disp, data[1] & 0x07)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "MOVEQ":
        length = 2
        operand = "#${0:02X},D{1:d}".format(data[1], (data[0] & 0x0e) >> 1)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("SBCD", "ABCD"):
        length = 2
        if data[1] & 0x08:
            operand = "-(A{0:d}),-(A{1:d})".format(data[1] & 0x07, (data[0] & 0x0e) >> 1)
        else:
            operand = "D{0:d},D{1:d}".format(data[1] & 0x07, (data[0] & 0x0e) >> 1)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "EXG":
        length = 2
        m = (data[1] & 0xf8) >> 3
        if m == 0x08:
            operand = "D{0:d},D{1:d}".format((data[0] & 0x0e) >> 1, data[1] & 0x07)
        elif m == 0x09:
            operand = "A{0:d},A{1:d}".format((data[0] & 0x0e) >> 1, data[1] & 0x07)
        elif m == 0x11:
            operand = "D{0:d},A{1:d}".format((data[0] & 0x0e) >> 1, data[1] & 0x07)
        else:
            print("Error: internal error (should never occur)", mnemonic)

        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: ASd, LSd, ROXd, ROd
    elif mnemonic in ("ASD", "LSD", "ROXD", "ROD") and ((data[1] & 0xc0) >> 6) != 3:
        length = 2
        cr = (data[0] & 0x0e) >> 1
        dr = data[0] & 0x01
        size = (data[1] & 0xc0) >> 6
        ir = (data[1] & 0x20) >> 5
        reg = data[1] & 0x07

        # Handle direction
        if dr == 1:
            mnemonic = mnemonic.replace(mnemonic[len(mnemonic)-1], 'L')  # left
        else:
            mnemonic = mnemonic.replace(mnemonic[len(mnemonic)-1], 'R')  # right

        # Handle size
        mnemonic += "." + SLength1(size)

        if ir == 1:  # Register shift
            operand = "D{0:d},D{1:d}".format(cr, reg)
        else:  # Immediate shift.
            if cr == 0:  # Shift count of zero means 8.
                cr = 8
            operand = "#{0:d},D{1:d}".format(cr, reg)

        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("ADDX", "SUBX"):
        length = 2
        size = (data[1] & 0xc0) >> 6
        mnemonic += "." + SLength1(size)

        if data[1] & 0x08:
            operand = "-(A{0:d}),-(A{1:d})".format(data[1] & 0x07, (data[0] & 0x0e) >> 1)
        else:
            operand = "D{0:d},D{1:d}".format(data[1] & 0x07, (data[0] & 0x0e) >> 1)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "CMPM":
        length = 2
        size = (data[1] & 0xc0) >> 6
        mnemonic += "." + SLength1(size)

        operand = "(A{0:d})+,(A{1:d})+".format(data[1] & 0x07, (data[0] & 0x0e) >> 1)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("JMP", "JSR"):
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        if m == 2:  # (An)
            length = 2
            operand = "(A{0:d})".format(xn)
        elif m == 5:  # d16(An)
            length = 4
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            operand = "${0:02X}{1:02X}(A{2:d})".format(data[2], data[3], xn)
        elif m == 6:  # d8(An,Xn)
            length = 4
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            if data[2] & 0x80:
                operand = "${0:02X}(A{1:d},A{2:d})".format(data[3], xn, (data[2] & 0x70) >> 4)
            else:
                operand = "${0:02X}(A{1:d},D{2:d})".format(data[3], xn, (data[2] & 0x70) >> 4)
        elif m == 7 and xn == 2:  # d16(pc)
            length = 4
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            operand = "${0:02X}{1:02X}(PC)".format(data[2], data[3])
        elif m == 7 and xn == 3:  # d8(PC,Xn)
            length = 4
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            if data[2] & 0x80:
                operand = "${0:02X}(PC,A{1:d})".format(data[3], (data[2] & 0x70) >> 4)
            else:
                operand = "${0:02X}(PC,D{1:d})".format(data[3], (data[2] & 0x70) >> 4)
        elif m == 7 and xn == 0:  # XXX.W
            length = 4
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            operand = "${0:02X}{1:02X}".format(data[2], data[3])
        elif m == 7 and xn == 1:  # XXX.L
            length = 6
            data[2] = ord(f.read(1))
            data[3] = ord(f.read(1))
            data[4] = ord(f.read(1))
            data[5] = ord(f.read(1))
            operand = "${0:02X}{1:02X}{2:02X}{3:02X}".format(data[2], data[3], data[4], data[5])
        else:
            print("Error: Invalid addressing mode.")
            length = 2
            operand = ""
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("ORI", "ANDI", "SUBI", "ADDI", "EORI", "CMPI"):
        s = (data[1] & 0xc0) >> 6
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength(SLength1(s), m, xn) + 2

        if s == 2:  # L
            length += 2

        for i in range(2, length):
            data[i] = ord(f.read(1))

        if s == 0:  # B
            mnemonic += ".b"
            src = "#${0:02X}".format(data[3])
        elif s == 1:  # W
            mnemonic += ".w"
            src = "#${0:02X}{1:02X}".format(data[2], data[3])
        elif s == 2:  # L
            mnemonic += ".l"
            src = "#${0:02X}{1:02X}{2:02X}{3:02X}".format(data[2], data[3], data[4], data[5])
        else:
            print("Error: Invalid instruction size.")

        dest = EffectiveAddress(SLength1(s), m, xn)
        operand = src + "," + dest
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("BTST", "BCLR", "BCHG", "BSET"):
        dn = (data[0] & 0x0e) >> 1
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength('l', m, xn)

        if data[0] == 0x08:  # Immediate
            length += 2

        for i in range(2, length):
            data[i] = ord(f.read(1))

        # Source:
        # BTST  #data, <ea>  0000100000MMMXXX
        # BTST  Dn, <ea>     0000DDD100MMMXXX

        if data[0] == 0x08:  # Immediate
            src = "#${0:02X}".format(data[3])
        else:
            src = "D{0:d}".format(dn)

        dest = EffectiveAddress(SLength1(s), m, xn)
        operand = src + "," + dest
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("TST", "NEGX", "CLR", "NEG", "NOT"):
        s = (data[1] & 0xc0) >> 6
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength(SLength1(s), m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        mnemonic += "." + SLength1(s)

        dest = EffectiveAddress(SLength1(s), m, xn)
        printInstruction(address, length, mnemonic, data, dest)

    # Handle instruction types: MOVE from SR/to SR
    elif mnemonic in ("MOVE from SR", "MOVE to CCR", "MOVE to SR"):
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength("b", m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        dest = EffectiveAddress("b", m, xn)

        if mnemonic == "MOVE from SR":
            mnemonic = "MOVE"
            operand = "sr," + dest
        elif mnemonic == "MOVE to CCR":
            mnemonic = "MOVE"
            operand = dest + ",ccr"
        elif mnemonic == "MOVE to SR":
            mnemonic = "MOVE"
            operand = dest + ",sr"

        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: NBCD
    elif mnemonic in ("NBCD", "PEA", "TAS"):
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength(SLength1(s), m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress(SLength1(s), m, xn)
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: ASd, LSd, ROXd, ROd
    elif mnemonic in ("ASD", "LSD", "ROXD", "ROD") and ((data[1] & 0xc0) >> 6) == 3:
        d = data[0] & 0x01
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        # Handle direction
        if d == 1:
            mnemonic = mnemonic.replace(mnemonic[len(mnemonic)-1], 'L')  # left
        else:
            mnemonic = mnemonic.replace(mnemonic[len(mnemonic)-1], 'R')  # right

        length = InstructionLength(SLength1(s), m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress(SLength1(s), m, xn)
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: ADDA, CMPA, SUBA
    elif mnemonic in ("ADDA", "CMPA", "SUBA"):
        an = (data[0] & 0xe) >> 1
        s = data[0] & 0x01
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        # Handle size
        mnemonic += "." + SLength3(s)

        length = InstructionLength(SLength3(s), m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress(SLength3(s), m, xn)
        operand = operand + ",A{0:n}".format(an)
        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: MOVEM
    elif mnemonic == "MOVEM":
        d = (data[0] & 0x04) >> 2
        s = (data[1] & 0x40) >> 6
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        # Handle size
        mnemonic += "." + SLength3(s)

        length = InstructionLength(SLength1(s), m, xn) + 2

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress(SLength1(s), m, xn)
        regs = 256 * data[2] + data[3]  # Register list
        if d == 0:
            operand = registerList(m == 4, regs) + "," + operand
        else:
            operand = operand + "," + registerList(m == 4, regs)

        printInstruction(address, length, mnemonic, data, operand)

    # Handle instruction types: MOVEA
    elif mnemonic == "MOVEA":
        s = (data[0] & 0x30) >> 4
        an = (data[0] & 0xe) >> 1
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        # Handle size
        mnemonic += "." + SLength2(s)

        length = InstructionLength(SLength2(s), m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress(SLength2(s), m, xn)
        operand = operand + ",A{0:n}".format(an)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "MOVE":
        s = (data[0] & 0x30) >> 4
        dxn = (data[0] & 0xe) >> 1
        dm = ((data[1] & 0xc0) >> 6) + ((data[0] & 0x01) << 2)
        sxn = data[1] & 0x07
        sm = (data[1] & 0x38) >> 3

        # Handle size
        mnemonic += "." + SLength2(s)

        # Get length based on source addressing mode
        length = InstructionLength(SLength2(s), sm, sxn)

        # Adjust instruction length based on destination addressing mode
        if dm == 2 and SLength2(s) != "l" and dm == 7 and dxn == 1:  # (An) and byte or word size -> subtract two if source mode is abs.L
            length -= 2
        elif dm == 5:  # d16(An) -> add 2
            length += 2
        elif dm == 6:  # d8(An,Xn) -> add 2
            length += 2
        elif dm == 7 and dxn == 0:  # abs.W -> add 2
            length += 2
        elif dm == 7 and dxn == 1:  # abs.L -> add 4
            length += 4

        for i in range(2, length):
            data[i] = ord(f.read(1))

        # Handle some special cases.
        if sm == 7 and sxn == 1:  # Source is abs.L
            src = "${0:02X}{1:02X}{2:02X}{3:02X}".format(data[length-8], data[length-7], data[length-6], data[length-5])
        elif sm == 7 and sxn == 4 and SLength2(s) == "l":  # Source is #imm long
            operand = "#${0:02X}{1:02X}{2:02X}{3:02X}".format(data[length-8], data[length-7], data[length-6], data[length-5])
        else:
            src = EffectiveAddress(SLength2(s), sm, sxn)

        dest = EffectiveAddress(SLength2(s), dm, dxn)

        operand = src + "," + dest
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "LEA":
        an = (data[0] & 0xe) >> 1
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength("l", m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress("l", m, xn)
        operand = operand + ",A{0:n}".format(an)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "CHK":
        dn = (data[0] & 0xe) >> 1
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength("w", m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        operand = EffectiveAddress("w", m, xn)
        operand = operand + ",D{0:n}".format(dn)
        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic in ("ADDQ", "SUBQ"):
        s = (data[1] & 0xc0) >> 6
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07
        add = (data[0] & 0x0e) >> 1

        if add == 0:
            add = 8

        length = InstructionLength(SLength1(s), m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        mnemonic += "." + SLength1(s)

        src = "#{0:d}".format(add)
        dest = EffectiveAddress(SLength1(s), m, xn)
        operand = src + "," + dest

        printInstruction(address, length, mnemonic, data, operand)

    elif mnemonic == "SCC":
        cond = data[0] & 0x0f
        m = (data[1] & 0x38) >> 3
        xn = data[1] & 0x07

        length = InstructionLength("b", m, xn)

        for i in range(2, length):
            data[i] = ord(f.read(1))

        mnemonic = "S" + conditions[cond]
        operand = EffectiveAddress("b", m, xn)
        printInstruction(address, length, mnemonic, data, operand)

    else:
        print("Error: unsupported instruction", mnemonic)

    # Do next instruction
    address += length
    length = 0
    opcode = 0
    mnemonic = ""
    operand = ""
