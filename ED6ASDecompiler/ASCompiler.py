import struct
from ED6ASInstructionsSet import Type, operand

class BinASFile(object):
    def __init__(self, name):
        self.bin_strings = bytes()
        self.bin_strings2 = bytes()
        self.bin_chip_ids = bytes()
        self.bin_functions = [] #will contain the binary content of each function separately, and then we will "share" the pointers of the identical ones
        self.bin_no_idea_bytes = bytes() 
        self.locations = []

currentASFile = BinASFile("dummy")
current_bin_function = bytes()
current_function_id = -1
function_addrs = []
current_addr = 0
bin_map = {}
map_id_ptr = {} #key : id, value : ptr
map_loc = {} #key : loc, value : ptr


def set_chips(chip_ids):
    global currentASFile
    for chip_id in chip_ids:
        chip_bin = struct.pack("<I",chip_id)
        currentASFile.bin_chip_ids = currentASFile.bin_chip_ids + chip_bin

def set_strings(strings):
    global currentASFile
    for str in strings:
        currentASFile.bin_strings = currentASFile.bin_strings + bytes(str.encode("cp932")) + bytes(struct.pack("<B",0))
    currentASFile.bin_strings = currentASFile.bin_strings + bytes(struct.pack("<B",0))
def set_strings2(value, strings):
    global currentASFile
    currentASFile.bin_strings2 = currentASFile.bin_strings2 + bytes(struct.pack("<B",value))
    for str in strings:
        currentASFile.bin_strings2 = currentASFile.bin_strings2 + bytes(str.encode("cp932")) + bytes(struct.pack("<B",0))
    if len(strings) > 0:
        currentASFile.bin_strings2 = currentASFile.bin_strings2 + bytes(struct.pack("<B",0))
def set_mysterious_bytes(bs):
    global currentASFile
    currentASFile.bin_no_idea_bytes = bytes(bs)

def set_script(name):
    global currentASFile
    currentASFile.name = name

def add_locations(names):
    global currentASFile
    currentASFile.locations = names

def SetLoc(name):
    global map_loc
    global current_addr

    map_loc[name] = current_addr

    
    

def compile_str(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(value.encode("cp932")) + bytes(struct.pack("<B",0))

def compile_fixed_length(value, size):
    global current_bin_function
    bin_text = bytes(value.encode("cp932"))
    current_bin_function = current_bin_function + bin_text
    to_pad = size - len(bin_text)
    pad_array = bytes()
    for i in range(to_pad):
        pad_array.append(0)
    current_bin_function = current_bin_function + pad_array

def compile_s16(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(struct.pack("<h",value))

def compile_u8(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(struct.pack("<B",value))

def compile_u16(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(struct.pack("<H",value))

def compile_u32(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(struct.pack("<I",value))

def compile_s32(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(struct.pack("<i",value))
    
def compile_float(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytes(struct.pack("<f",value))

def compile_arg(op):
    if (op.type == Type.FLOAT):
        compile_float(op.value)
    elif (op.type == Type.S16):
        compile_s16(op.value)
    elif (op.type == Type.S32):
        compile_s32(op.value)
    elif (op.type == Type.STR):
        compile_str(op.value)
    elif (op.type == Type.STRFIXED):
        compile_fixed_length(op.value, op.bytes_length)
    elif (op.type == Type.U8):
        compile_u8(op.value)
    elif (op.type == Type.U16):
        compile_u16(op.value)
    elif (op.type == Type.U32):
        compile_u32(op.value)

def FIXED_LENGTH(value, sz):
    return operand(None, None, value, Type.STRFIXED, sz)
def SIGNED_16(value):
    return operand(None, None, value, Type.S16)
def SIGNED_32(value):
    return operand(None, None, value, Type.S32)
def U8(value):
    return operand(None, None, value, Type.U8)
def U16(value):
    return operand(None, None, value, Type.U16)
def U32(value):
    return operand(None, None, value, Type.U32)
def FLOAT(value):
    return operand(None, None, value, Type.FLOAT)


def compile_function(OP, args):
    global current_bin_function
    global current_addr
    current_bin_function = current_bin_function + bytearray(struct.pack("<B",OP))
    for arg in args:
        if (type(arg) == str):
            compile_arg(operand(None, None, arg, Type.STR))
        else:
            compile_arg(arg)

    current_addr = len(current_bin_function)

def assemble():
    global current_function_id
    global currentASFile
    global current_bin_function
    #if (current_function_id > -1):
    #    if current_bin_function in bin_map.keys():
    #        bin_map[current_bin_function].push_back(current_function_id)
    #    else:
    #        bin_map[current_bin_function] = [current_function_id]
    #
    map_ptr_bytes = {} #key : ptr, value : content

    addr_ptrs = 6 + len(currentASFile.bin_chip_ids) + 4 + len(currentASFile.bin_strings)+ len(currentASFile.bin_strings2)
    
    second_addr = addr_ptrs + len(currentASFile.locations) * 2
    actual_function_start = second_addr + 0x10
    current_addr = actual_function_start
    #for id in function_ids:
    #    if id not in map_id_ptr.keys():
    #        for k in bin_map.items():
    #            if id in k[1]:
    #                for k2 in k[1]:
    #                    map_id_ptr[k2] = current_addr
    #                map_ptr_bytes[current_addr] = k[0]
    #                current_addr = current_addr + len(k[0])
    #                break
    #
    
    if len(currentASFile.bin_strings2) > 0:
        third_addr = 6 + len(currentASFile.bin_chip_ids) + 4 + len(currentASFile.bin_strings)
    else:
        third_addr = 0

    bin_ptrs = bytes()
    for loc in currentASFile.locations:
        bin_ptrs = bin_ptrs + bytes(struct.pack("<H", map_loc[loc] + actual_function_start))

    file = bytes(struct.pack("<H",addr_ptrs))
    file = file + bytes(struct.pack("<H",second_addr))
    file = file + bytes(struct.pack("<H",third_addr))
    file = file + currentASFile.bin_chip_ids
    file = file + bytes(struct.pack("<I",0xFFFFFFFF))
    file = file + currentASFile.bin_strings
    file = file + currentASFile.bin_strings2
    file = file + bin_ptrs
    file = file + currentASFile.bin_no_idea_bytes

    current_addr = len(file)

    file = file + current_bin_function
    #while current_addr in map_ptr_bytes.keys():
    #    file = file + map_ptr_bytes[current_addr]
    #    current_addr = len(file)

    as_file = open(currentASFile.name + "._DT", "wb")
    as_file.write(file)
    as_file.close()





#All the compile functions, ideally you have a custom way to compile them but I keep them generic because super lazy
def OP_00(args = []):
    compile_function(0, args)
def OP_01(args = []):
    compile_function(0x1, args)
def OP_02(args = []):
    compile_function(0x2, args)
def OP_03(args = []):
    compile_function(0x3, args)
def OP_04(args = []):
    compile_function(0x4, args)
def OP_05(args = []):
    compile_function(0x5, args)
def OP_06(args = []):
    compile_function(0x6, args)
def OP_07(args = []):
    compile_function(0x7, args)
def OP_08(args = []):
    compile_function(0x8, args)
def OP_09(args = []):
    compile_function(0x9, args)
def OP_0A(args = []):
    compile_function(0xA, args)
def OP_0B(args = []):
    compile_function(0xB, args)
def OP_0C(args = []):
    compile_function(0xC, args)
def OP_0D(args = []):
    compile_function(0xD, args)
def OP_0E(args = []):
    compile_function(0xE, args)
def OP_0F(args = []):
    compile_function(0xF, args)
def OP_10(args = []):
    compile_function(0x10, args)
def OP_11(args = []):
    compile_function(0x11, args)
def OP_12(args = []):
    compile_function(0x12, args)
def OP_13(args = []):
    compile_function(0x13, args)
def OP_14(args = []):
    compile_function(0x14, args)
def OP_15(args = []):
    compile_function(0x15, args)
def OP_16(args = []):
    compile_function(0x16, args)
def OP_17(args = []):
    compile_function(0x17, args)
def OP_18(args = []):
    compile_function(0x18, args)
def OP_19(args = []):
    compile_function(0x19, args)
def OP_1A(args = []):
    compile_function(0x1A, args)
def OP_1B(args = []):
    compile_function(0x1B, args)
def OP_1C(args = []):
    compile_function(0x1C, args)
def OP_1D(args = []):
    compile_function(0x1D, args)
def OP_1E(args = []):
    compile_function(0x1E, args)
def OP_1F(args = []):
    compile_function(0x1F, args)
def OP_20(args = []):
    compile_function(0x20, args)
def OP_21(args = []):
    compile_function(0x21, args)
def OP_22(args = []):
    compile_function(0x22, args)
def OP_23(args = []):
    compile_function(0x23, args)
def OP_24(args = []):
    compile_function(0x24, args)
def OP_25(args = []):
    compile_function(0x25, args)
def OP_26(args = []):
    compile_function(0x26, args)
def OP_27(args = []):
    compile_function(0x27, args)
def ShowText(args = []):
    compile_function(0x28, args)
def OP_29(args = []):
    compile_function(0x29, args)
def OP_2A(args = []):
    compile_function(0x2A, args)
def OP_2B(args = []):
    compile_function(0x2B, args)
def OP_2C(args = []):
    compile_function(0x2C, args)
def OP_2D(args = []):
    compile_function(0x2D, args)
def OP_2E(args = []):
    compile_function(0x2E, args)
def OP_2F(args = []):
    compile_function(0x2F, args)
def OP_30(args = []):
    compile_function(0x30, args)
def OP_31(args = []):
    compile_function(0x31, args)
def OP_32(args = []):
    compile_function(0x32, args)
def OP_33(args = []):
    compile_function(0x33, args)
def OP_34(args = []):
    compile_function(0x34, args)
def OP_35(args = []):
    compile_function(0x35, args)
def OP_36(args = []):
    compile_function(0x36, args)
def OP_37(args = []):
    compile_function(0x37, args)
def OP_38(args = []):
    compile_function(0x38, args)
def OP_39(args = []):
    compile_function(0x39, args)
def OP_3A(args = []):
    compile_function(0x3A, args)
def OP_3B(args = []):
    compile_function(0x3B, args)
def OP_3C(args = []):
    compile_function(0x3C, args)
def OP_3D(args = []):
    compile_function(0x3D, args)
def OP_3E(args = []):
    compile_function(0x3E, args)
def OP_3F(args = []):
    compile_function(0x3F, args)
def OP_40(args = []):
    compile_function(0x40, args)
def OP_41(args = []):
    compile_function(0x41, args)
def OP_42(args = []):
    compile_function(0x42, args)
def OP_43(args = []):
    compile_function(0x43, args)
def OP_44(args = []):
    compile_function(0x44, args)
def OP_45(args = []):
    compile_function(0x45, args)
def OP_46(args = []):
    compile_function(0x46, args)
def OP_47(args = []):
    compile_function(0x47, args)
def OP_48(args = []):
    compile_function(0x48, args)
def OP_49(args = []):
    compile_function(0x49, args)
def OP_4A(args = []):
    compile_function(0x4A, args)
def OP_4B(args = []):
    compile_function(0x4B, args)
def OP_4C(args = []):
    compile_function(0x4C, args)
def OP_4D(args = []):
    compile_function(0x4D, args)
def OP_4E(args = []):
    compile_function(0x4E, args)
def OP_4F(args = []):
    compile_function(0x4F, args)
def OP_50(args = []):
    compile_function(0x50, args)
def OP_51(args = []):
    compile_function(0x51, args)
def OP_52(args = []):
    compile_function(0x52, args)
def OP_53(args = []):
    compile_function(0x53, args)
def OP_54(args = []):
    compile_function(0x54, args)
def OP_55(args = []):
    compile_function(0x55, args)
def OP_56(args = []):
    compile_function(0x56, args)
def OP_57(args = []):
    compile_function(0x57, args)
def OP_58(args = []):
    compile_function(0x58, args)
def OP_59(args = []):
    compile_function(0x59, args)
def OP_5A(args = []):
    compile_function(0x5A, args)
def OP_5B(args = []):
    compile_function(0x5B, args)
def OP_5C(args = []):
    compile_function(0x5C, args)
def OP_5D(args = []):
    compile_function(0x5D, args)
def OP_5E(args = []):
    compile_function(0x5E, args)
def OP_5F(args = []):
    compile_function(0x5F, args)
def OP_60(args = []):
    compile_function(0x60, args)
def OP_61(args = []):
    compile_function(0x61, args)
def OP_62(args = []):
    compile_function(0x62, args)
def OP_63(args = []):
    compile_function(0x63, args)
def OP_64(args = []):
    compile_function(0x64, args)
def OP_65(args = []):
    compile_function(0x65, args)
def OP_66(args = []):
    compile_function(0x66, args)
def OP_67(args = []):
    compile_function(0x67, args)
def OP_68(args = []):
    compile_function(0x68, args)
def OP_69(args = []):
    compile_function(0x69, args)
def OP_6A(args = []):
    compile_function(0x6A, args)
def OP_6B(args = []):
    compile_function(0x6B, args)
def OP_6C(args = []):
    compile_function(0x6C, args)
def OP_6D(args = []):
    compile_function(0x6D, args)
def OP_6E(args = []):
    compile_function(0x6E, args)
def OP_6F(args = []):
    compile_function(0x6F, args)
def OP_70(args = []):
    compile_function(0x70, args)
def OP_71(args = []):
    compile_function(0x71, args)
def OP_72(args = []):
    compile_function(0x72, args)
def OP_73(args = []):
    compile_function(0x73, args)
def OP_74(args = []):
    compile_function(0x74, args)
def OP_75(args = []):
    compile_function(0x75, args)
def OP_76(args = []):
    compile_function(0x76, args)
def OP_77(args = []):
    compile_function(0x77, args)
def OP_78(args = []):
    compile_function(0x78, args)
def OP_79(args = []):
    compile_function(0x79, args)
def OP_7A(args = []):
    compile_function(0x7A, args)
def OP_7B(args = []):
    compile_function(0x7B, args)
def OP_7C(args = []):
    compile_function(0x7C, args)
def OP_7D(args = []):
    compile_function(0x7D, args)
def OP_7E(args = []):
    compile_function(0x7E, args)
def OP_7F(args = []):
    compile_function(0x7F, args)
def OP_80(args = []):
    compile_function(0x80, args)
def OP_81(args = []):
    compile_function(0x81, args)
def OP_82(args = []):
    compile_function(0x82, args)
def OP_83(args = []):
    compile_function(0x83, args)
def OP_84(args = []):
    compile_function(0x84, args)
def OP_85(args = []):
    compile_function(0x85, args)
def OP_86(args = []):
    compile_function(0x86, args)
def OP_87(args = []):
    compile_function(0x87, args)
def OP_88(args = []):
    compile_function(0x88, args)
def OP_89(args = []):
    compile_function(0x89, args)

