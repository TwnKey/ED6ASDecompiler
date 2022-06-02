import os
from pathlib import Path
from utils import *
import ED6ASInstructionsSet

class function(object):
    def __init__(self, addr, ID):
        self.ID = ID
        self.addr_start = addr
        self.addr_end = -1
        self.instructions = []

    def add_instructions(self, content):
        current_addr = self.addr_start
        while current_addr < self.addr_end:
            instr = ED6ASInstructionsSet.instruction(content, current_addr)
            self.instructions.append(instr)
            current_addr = instr.end_addr

def decompile(file):
    

    
    filename = Path(file).stem
    filesize = os.path.getsize(file)
    f = open(file, 'rb')
    data = bytearray(f.read())
    first_sec_addr = read_int(data, 0, 2)
    second_sec_addr = read_int(data, 2, 2)
    uint16_0 = read_int(data, 4, 2)

    #reading the first section
    chip_ids = []
    current_addr = 6
    current_chip_id = read_int(data, current_addr, 4)
    while (current_chip_id != 0xFFFFFFFF):
        chip_ids.append(current_chip_id)
        current_chip_id = read_int(data, current_addr, 4)
        current_addr = current_addr + 4
    current_addr = current_addr + 4

    strings = []
    while (current_addr < first_sec_addr):
        output = []
        char = data[current_addr]
        text_size = 0
        while char != 0:
            text_size = text_size + 1
            output.append(char)
            current_addr = current_addr + 1
            char = data[current_addr]
        current_addr = current_addr + 1
        text_size = text_size + 1
        str = bytes(output).decode("cp932")
        strings.append(str)


    functions = []

    current_addr = first_sec_addr
    ID_fun = 0 

    while (current_addr < second_sec_addr):
        ptr = read_int(data, current_addr, 2)
        functions.append(function(ptr, ID_fun))
        ID_fun = ID_fun + 1
        current_addr = current_addr + 2

    no_idea_bytes = []
    current_addr = second_sec_addr
    for i in range(0x10):
        no_idea_bytes.append(read_int(data, current_addr + i, 1))

    current_addr = current_addr + 0x10

    functions.sort(key=lambda fun: fun.addr_start) 



    for i_fun in range(0, len(functions)-1): 
        functions[i_fun].addr_end = functions[i_fun + 1].addr_start
    functions[len(functions)-1].addr_end = filesize

    functions.sort(key=lambda fun: fun.ID) 

    for fun in functions:

        fun.add_instructions(data)





