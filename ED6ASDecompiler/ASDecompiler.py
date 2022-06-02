import os
from pathlib import Path
from utils import *
from array import array
from ED6ASInstructionsSet import instruction

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

def decompile(file):
    data = array('B')
    filename = Path(file).stem
    filesize = os.path.getsize(file)
    

    with open(file, 'rb') as f:
        data.fromfile(f, filesize)

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

    function_dic = {} #Key: ID, Value: Function

    current_addr = first_sec_addr
    ID_fun = 0 

    while (current_addr < second_sec_addr):
        ptr = read_int(data, current_addr, 2)
        function_dic[ID_fun] = function(ptr, ID_fun)
        ID_fun = ID_fun + 1
        current_addr = current_addr + 2

    no_idea_bytes = []
    current_addr = second_sec_addr
    for i in range(0x10):
        no_idea_bytes.append(read_int(data, current_addr + i, 1))

    current_addr = current_addr + 0x10

    functions_sorted_by_addr = function_ptrs.copy()
    functions_sorted_by_addr.sort(key=lambda fun: fun.addr_start) 



    for i_fun in range(0, functions_sorted_by_addr.size()-1):
        fun = functions_sorted_by_addr[i_fun]
        function_dic[fun.ID].addr_end = functions_sorted_by_addr[i_fun + 1].addr_start

    fun = functions_sorted_by_addr[functions_sorted_by_addr.size()-1]
    function_dic[fun.ID].addr_end = filesize

    for fun in function_dic:
        fun.add_instructions(data)

    print(current_addr)




