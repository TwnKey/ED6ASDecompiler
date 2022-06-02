from enum import Enum
import struct

class Type(Enum):
    FLOAT = 1
    S16 = 2
    S32 = 3
    STR = 4
    STRFIXED = 5
    U8 = 6
    U16 = 7
    U32 = 8


class operand:
    def __init__(self, addr, content, type, fixed_length = -1):

        self.bytes_length = fixed_length
        self.type = type

        if (type == Type.FLOAT):
            self.value = struct.unpack("<f", content[addr:addr+4])[0]
            self.bytes_length = 4 
        elif (type == Type.S16):
            self.value = struct.unpack("<h", content[addr:addr+2])[0]
            self.bytes_length = 2 
        elif (type == Type.S32):
            self.value = struct.unpack("<i", content[addr:addr+4])[0]
            self.bytes_length = 4
        elif (type == Type.STR) or (type == Type.STRFIXED):
            output = []
            char = content[addr]
            text_size = 0
            
            while char != 0:
                text_size = text_size + 1
                output.append(char)
                addr = addr + 1
                char = content[addr]
            text_size = text_size + 1
            if (type == Type.STR):
                self.bytes_length = text_size

            self.value = bytes(output).decode("cp932")
        elif (type == Type.U8):
            self.value = content[addr]
            self.bytes_length = 1
        elif (type == Type.U16):
            self.value = struct.unpack("<H", content[addr:addr+2])[0]
            self.bytes_length = 2
        elif (type == Type.U32):
            self.value = struct.unpack("<I", content[addr:addr+4])[0]
            self.bytes_length = 4
        
def AddOperand(instr, addr, content, type)->int:
    op = operand(addr, content, type)
    instr.operands.append(op)
    return addr + op.bytes_length

def OP_00(instr, content) -> int:
    instr.name = "OP_00"
    current_addr = instr.addr + 1
    return current_addr 

def OP_01(instr, content) -> int:
    instr.name = "OP_01"
    current_addr = instr.addr + 1
    
    current_addr = AddOperand(instr, current_addr, content, Type.U16)

    return current_addr 

def OP_02(instr, content) -> int:
    instr.name = "OP_02"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr 
def OP_03(instr, content) -> int:
    instr.name = "OP_03"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr 
def OP_04(instr, content) -> int:
    instr.name = "OP_04"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr 
def OP_05(instr, content) -> int:
    instr.name = "OP_05"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 
def OP_06(instr, content) -> int:
    instr.name = "OP_06"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 

def OP_07(instr, content) -> int:
    instr.name = "OP_07"
    current_addr = instr.addr + 1
    return current_addr 

def OP_08(instr, content) -> int:
    instr.name = "OP_08"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.S16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 


def OP_09(instr, content) -> int:
    instr.name = "OP_09"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 

def OP_0A(instr, content) -> int:
    instr.name = "OP_0A"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 

def OP_0B(instr, content) -> int:
    instr.name = "OP_0B"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 

def OP_0C(instr, content) -> int:
    instr.name = "OP_0C"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.S16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr 
def OP_0E(instr, content) -> int:
    instr.name = "OP_0E"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    return current_addr 
def OP_11(instr, content) -> int:
    instr.name = "OP_11"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_12(instr, content) -> int:
    instr.name = "OP_12"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.STR)
    return current_addr
def OP_13(instr, content) -> int:
    instr.name = "OP_13"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_14(instr, content) -> int:
    instr.name = "OP_14"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr
def OP_15(instr, content) -> int:
    instr.name = "OP_15"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_16(instr, content) -> int:
    instr.name = "OP_16"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_17(instr, content) -> int:
    instr.name = "OP_17"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_18(instr, content) -> int:
    instr.name = "OP_18"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)   
    return current_addr


def OP_1B(instr, content) -> int:
    instr.name = "OP_1B"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_1C(instr, content) -> int:
    instr.name = "OP_1C"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_1D(instr, content) -> int:
    instr.name = "OP_1D"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_1E(instr, content) -> int:
    instr.name = "OP_1E"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    return current_addr

def OP_20(instr, content) -> int:
    instr.name = "OP_20"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_21(instr, content) -> int:
    instr.name = "OP_21"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    
    return current_addr


def OP_22(instr, content) -> int:
    instr.name = "OP_22"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    
    return current_addr
def OP_23(instr, content) -> int:
    instr.name = "OP_23"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_24(instr, content) -> int:
    instr.name = "OP_24"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr
def OP_25(instr, content) -> int:
    instr.name = "OP_25"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr
def OP_28(instr, content) -> int:
    instr.name = "ShowText"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.STR)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_29(instr, content) -> int:
    instr.name = "OP_29"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr
def OP_2C(instr, content) -> int:
    instr.name = "OP_2C"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr
def OP_2D(instr, content) -> int:
    instr.name = "OP_2D"
    current_addr = instr.addr + 1
    return current_addr
def OP_2E(instr, content) -> int:
    instr.name = "OP_2E"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    return current_addr

def OP_2F(instr, content) -> int:
    instr.name = "OP_2F"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr
def OP_31(instr, content) -> int:
    instr.name = "OP_31"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_33(instr, content) -> int:
    instr.name = "OP_33"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_34(instr, content) -> int:
    instr.name = "OP_34"
    current_addr = instr.addr + 1
    return current_addr
def OP_35(instr, content) -> int:
    instr.name = "OP_35"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_36(instr, content) -> int:
    instr.name = "OP_36"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_37(instr, content) -> int:
    instr.name = "OP_37"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    return current_addr

def OP_39(instr, content) -> int:
    instr.name = "OP_39"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    current_addr = AddOperand(instr, current_addr, content, Type.S32)
    return current_addr

def OP_3B(instr, content) -> int:
    instr.name = "OP_3B"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_3C(instr, content) -> int:
    instr.name = "OP_3C"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_3D(instr, content) -> int:
    instr.name = "OP_3D"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_3E(instr, content) -> int:
    instr.name = "OP_3E"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_3F(instr, content) -> int:
    instr.name = "OP_3F"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr
def OP_40(instr, content) -> int:
    instr.name = "OP_40"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_41(instr, content) -> int:
    instr.name = "OP_41"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_42(instr, content) -> int:
    instr.name = "OP_42"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_44(instr, content) -> int:
    instr.name = "OP_44"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_45(instr, content) -> int:
    instr.name = "OP_45"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_46(instr, content) -> int:
    instr.name = "OP_46"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_47(instr, content) -> int:
    instr.name = "OP_47"
    current_addr = instr.addr + 1
    return current_addr

def OP_4B(instr, content) -> int:
    instr.name = "OP_4B"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_4C(instr, content) -> int:
    instr.name = "OP_4C"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_4D(instr, content) -> int:
    instr.name = "OP_4D"
    current_addr = instr.addr + 1

    return current_addr

def OP_4E(instr, content) -> int:
    instr.name = "OP_4E"
    current_addr = instr.addr + 1

    return current_addr
def OP_50(instr, content) -> int:
    instr.name = "OP_50"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_51(instr, content) -> int:
    instr.name = "OP_51"
    current_addr = instr.addr + 1
    return current_addr

def OP_52(instr, content) -> int:
    instr.name = "OP_52"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_53(instr, content) -> int:
    instr.name = "OP_53"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr
def OP_54(instr, content) -> int:
    instr.name = "OP_54"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_55(instr, content) -> int:
    instr.name = "OP_55"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_56(instr, content) -> int:
    instr.name = "OP_56"
    current_addr = instr.addr + 1
    return current_addr

def OP_5A(instr, content) -> int:
    instr.name = "OP_5A"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_5B(instr, content) -> int:
    instr.name = "OP_5B"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_5C(instr, content) -> int:
    instr.name = "OP_5C"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_5D(instr, content) -> int:
    instr.name = "OP_5D"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr
def OP_5E(instr, content) -> int:
    instr.name = "OP_5E"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_5F(instr, content) -> int:
    instr.name = "OP_5F"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr
def OP_60(instr, content) -> int:
    instr.name = "OP_60"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_62(instr, content) -> int:
    instr.name = "OP_62"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_63(instr, content) -> int:
    instr.name = "OP_63"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_64(instr, content) -> int:
    instr.name = "OP_64"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    return current_addr

def OP_65(instr, content) -> int:
    instr.name = "OP_65"
    current_addr = instr.addr + 1

    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_67(instr, content) -> int:
    instr.name = "OP_67"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.STR)
    return current_addr
def OP_69(instr, content) -> int:
    instr.name = "OP_69"
    current_addr = instr.addr + 1
    return current_addr
def OP_6A(instr, content) -> int:
    instr.name = "OP_6A"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr


def OP_6C(instr, content) -> int:
    instr.name = "OP_6C"
    current_addr = instr.addr + 1

    return current_addr

def OP_78(instr, content) -> int:
    instr.name = "OP_78"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_7A(instr, content) -> int:
    instr.name = "OP_7A"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_80(instr, content) -> int:
    instr.name = "OP_80"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

def OP_84(instr, content) -> int:
    instr.name = "OP_84"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U8)
    return current_addr

def OP_87(instr, content) -> int:
    instr.name = "OP_87"
    current_addr = instr.addr + 1
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U16)
    current_addr = AddOperand(instr, current_addr, content, Type.U32)
    return current_addr

instruction_set = {
                0x00:OP_00,   #0x477FF0
                0x01:OP_01,   #0x478010
                0x02:OP_02,   #0x475A20
                0x03:OP_03,   #0x475C50
                0x04:OP_04,   #0x475E30
                0x05:OP_05,   #0x475F00
                0x06:OP_06,   #0x476120
                0x07:OP_07,   #0x4760F0
                0x08:OP_08,   #0x476160
                0x09:OP_09,   #0x476320
                0x0A:OP_0A,   #0x4763F0
                0x0B:OP_0B,   #0x476680
                0x0C:OP_0C,   #0x476950
                #0x0D:OP_0D,   #0x476B10
                0x0E:OP_0E,   #0x476C80
                #0x0F:OP_0F,   #0x476E10
                #0x10:OP_10,   #0x477060
                0x11:OP_11,   #0x477150
                0x12:OP_12,   #0x477410
                0x13:OP_13,   #0x4774A0
                0x14:OP_14,   #0x4774F0
                0x15:OP_15,   #0x477560
                0x16:OP_16,   #0x4775C0
                0x17:OP_17,   #0x4775F0
                0x18:OP_18,   #0x477620
                #0x19:OP_19,   #0x477AE0
                #0x1A:OP_1A,   #0x477E40
                0x1B:OP_1B,   #0x4759C0
                0x1C:OP_1C,   #0x478040
                0x1D:OP_1D,   #0x478110
                0x1E:OP_1E,   #0x478240
                #0x1F:OP_1F,   #0x478990
                0x20:OP_20,   #0x4784B0
                0x21:OP_21,   #0x478740
                0x22:OP_22,   #0x478A10
                0x23:OP_23,   #0x478AA0
                0x24:OP_24,   #0x478B20
                0x25:OP_25,   #0x478D40
                #0x26:OP_26,   #0x478E20
                #0x27:OP_27,   #0x478EB0
                0x28:OP_28,   #0x478F40
                0x29:OP_29,   #0x478FF0
                #0x2A:OP_2A,   #0x479070
                #0x2B:OP_2B,   #0x479180
                0x2C:OP_2C,   #0x4791F0
                0x2D:OP_2D,   #0x479250
                0x2E:OP_2E,   #0x479280
                0x2F:OP_2F,   #0x47A2A0
                #0x30:OP_30,   #0x47A340
                0x31:OP_31,   #0x479330
                #0x32:OP_32,   #0x47A420
                0x33:OP_33,   #0x47A460
                0x34:OP_34,   #0x479370
                0x35:OP_35,   #0x479390
                0x36:OP_36,   #0x479650
                0x37:OP_37,   #0x479720
                #0x38:OP_38,   #0x4797C0
                0x39:OP_39,   #0x4798B0
                #0x3A:OP_3A,   #0x479900
                0x3B:OP_3B,   #0x479950
                0x3C:OP_3C,   #0x4799A0
                0x3D:OP_3D,   #0x479A90
                0x3E:OP_3E,   #0x479B10
                0x3F:OP_3F,   #0x479B60
                0x40:OP_40,   #0x479CC0
                0x41:OP_41,   #0x479BA0
                0x42:OP_42,   #0x479C00
                #0x43:OP_43,   #0x479CF0
                0x44:OP_44,   #0x479D70
                0x45:OP_45,   #0x479E20
                0x46:OP_46,   #0x479E80
                0x47:OP_47,   #0x479EC0
                #0x48:OP_48,   #0x479F40
                #0x49:OP_49,   #0x479FA0
                #0x4A:OP_4A,   #0x47A250
                0x4B:OP_4B,   #0x47A4A0
                0x4C:OP_4C,   #0x47A770
                0x4D:OP_4D,   #0x47A7B0
                0x4E:OP_4E,   #0x47A7D0
                #0x4F:OP_4F,   #0x47A7F0
                0x50:OP_50,   #0x47A850
                0x51:OP_51,   #0x47A8B0
                0x52:OP_52,   #0x47A8F0
                0x53:OP_53,   #0x47A910
                0x54:OP_54,   #0x47A940
                0x55:OP_55,   #0x47A990
                0x56:OP_56,   #0x47AA00
                #0x57:OP_57,   #0x47AA50
                #0x58:OP_58,   #0x47AAD0
                #0x59:OP_59,   #0x47AAF0
                0x5A:OP_5A,   #0x47AB20
                0x5B:OP_5B,   #0x47AB60
                0x5C:OP_5C,   #0x47AB90
                0x5D:OP_5D,   #0x47AC10
                0x5E:OP_5E,   #0x47AC90
                0x5F:OP_5F,   #0x47AD30
                0x60:OP_60,   #0x47AE20
                #0x61:OP_61,   #0x47AEE0
                0x62:OP_62,   #0x47AF20
                0x63:OP_63,   #0x47AFD0
                0x64:OP_64,   #0x47B070
                0x65:OP_65,   #0x47B0B0
                #0x66:OP_66,   #0x47B120
                0x67:OP_67,   #0x47B150
                #0x68:OP_68,   #0x47B230
                0x69:OP_69,   #0x47B240
                0x6A:OP_6A,   #0x47B270
                #0x6B:OP_6B,   #0x47B2B0
                0x6C:OP_6C,   #0x47B300
                #0x6D:OP_6D,   #0x47B340
                #0x6E:OP_6E,   #0x47B370
                #0x6F:OP_6F,   #0x47B3A0
                #0x70:OP_70,   #0x47B400
                #0x71:OP_71,   #0x47B7F0
                #0x72:OP_72,   #0x47B870
                #0x73:OP_73,   #0x47B8E0
                #0x74:OP_74,   #0x47B8A0
                #0x75:OP_75,   #0x47B920
                #0x76:OP_76,   #0x47B950
                #0x77:OP_77,   #0x47B980
                0x78:OP_78,   #0x47B9D0
                #0x79:OP_79,   #0x47BA30
                0x7A:OP_7A,   #0x47BA40
                #0x7B:OP_7B,   #0x475A80
                #0x7C:OP_7C,   #0x475AF0
                #0x7D:OP_7D,   #0x475B20
                #0x7E:OP_7E,   #0x475B40
                #0x7F:OP_7F,   #0x47BA70
                0x80:OP_80,   #0x4782F0
                #0x81:OP_81,   #0x4783D0
                #0x82:OP_82,   #0x478430
                #0x83:OP_83,   #0x47BAC0
                0x84:OP_84,   #0x47BB30
                #0x85:OP_85,   #0x47BC70
                #0x86:OP_86,   #0x47BE50
                0x87:OP_87,   #0x47BEC0
                #0x88:OP_88,   #0x47BF60
                #0x89:OP_89,   #0x47BFA0 
}



class instruction(object):
    """description of class"""
    def __init__(self, content, addr):
        self.addr = addr 
        self.op_code = content[addr]
        self.operands = []
        self.name = ""
        self.text_before = ""
        print(hex(addr), " ", hex(self.op_code))
        try:
            self.end_addr = instruction_set[self.op_code](self, content)
        except:
            raise Exception("Wrong OP Code ", hex(self.op_code), " at addr ", hex(self.addr))


    def to_string(self, stream)->str:
        result = self.text_before + self.name + "("
        for operand_id in range(len(self.operands)-1):
            value = self.operands[operand_id].value
            if (type(value) == str):
                result = result + "\"" + value + "\""
            else:
                result = result + str(int(value))
            result = result + ", "
        if len(self.operands) > 0:
            value = self.operands[len(self.operands)-1].value
            if (type(value) == str):
                result = result + "\"" + value + "\""
            else:
                result = result + str(int(value))
        result = result + ")"
        return result
