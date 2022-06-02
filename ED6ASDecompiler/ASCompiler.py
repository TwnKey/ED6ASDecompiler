import struct

class BinASFile(object):
    def __init__(self, name):
        self.bin_strings = bytearray()
        self.bin_chip_ids = bytearray()
        self.bin_functions = bytearray()
        self.bin_no_idea_bytes = [] #will contain the binary content of each function separately, and then we will "share" the pointers of the identical ones

currentASFile = BinASFile("dummy")
current_bin_function = bytearray()
current_function_id = -1

def set_chips(chip_ids):
    global currentASFile
    for chip_id in chip_ids:
        chip_bin = struct.pack("<I",chip_id)
        currentASFile.bin_chip_ids = currentASFile.bin_chip_ids + chip_bin

def set_strings(strings):
    global currentASFile
    for str in strings:
        currentASFile.strings = currentASFile.strings + bytearray(s.encode("cp932"))

def set_mysterious_bytes(bytes):
    global currentASFile
    currentASFile.bin_no_idea_bytes = bytearray(bytes)

def set_script(name):
    global currentASFile
    currentASFile.name = name

def set_current_function(id):
    global current_function_id
    global currentASFile
    global current_bin_function
    if (current_function_id > -1):
        currentASFile.bin_functions.append(current_bin_function)

    current_function_id = id 

def STR(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(value.encode("cp932"))

def FIXED_LENGTH(value, size):
    global current_bin_function
    bin_text = bytearray(value.encode("cp932"))
    current_bin_function = current_bin_function + bin_text
    to_pad = size - len(bin_text)
    pad_array = bytearray()
    for i in range(to_pad):
        pad_array.append(0)
    current_bin_function = current_bin_function + pad_array

def SIGNED_16(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(struct.pack("<h",value))

def U8(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(struct.pack("<B",value))

def U16(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(struct.pack("<H",value))

def U32(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(struct.pack("<I",value))

def SIGNED_32(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(struct.pack("<i",value))
    
def FLOAT(value):
    global current_bin_function
    current_bin_function = current_bin_function + bytearray(struct.pack("<f",value))