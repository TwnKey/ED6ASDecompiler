import os
from pathlib import Path
from utils import *
import ED6ASInstructionsSet

class ASFile(object):
    def __init__(self, name):
        self.name = name
        self.strings = []
        self.strings2 = []
        self.no_idea = None
        self.chip_ids = []
        self.fun = None
        self.locations_dict = {}
        self.locations = []
        self.no_idea_bytes = []

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
    def to_string(self, locations):
        result = ""
        for instr in self.instructions:
            if instr.addr in locations.keys():
                result = result + "\n    SetLoc(\"" + locations[instr.addr] + "\")\n\n"
            result = result + "    " + instr.to_string() + "\n"
        return result

def decompile(file):

    filename = Path(file).stem
    filesize = os.path.getsize(file)

    result = ASFile(filename)

    f = open(file, 'rb')
    data = bytearray(f.read())
    first_sec_addr = read_int(data, 0, 2)
    second_sec_addr = read_int(data, 2, 2)
    third_sec_addr = read_int(data, 4, 2)


    no_idea = None

    #reading the first section
    chip_ids = []
    current_addr = 6
    current_chip_id = read_int(data, current_addr, 4)
    while (current_chip_id != 0xFFFFFFFF):
        chip_ids.append(current_chip_id)
        current_addr = current_addr + 4
        current_chip_id = read_int(data, current_addr, 4)
        
    current_addr = current_addr + 4

    strings = []
    strings2 = []

    if third_sec_addr > 0:
        stop = third_sec_addr
    else:
        stop = first_sec_addr
    
    while (data[current_addr] != 0):
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
        str_ = bytes(output).decode("cp932")
        strings.append(str_.replace("\\", "\\\\"))

    current_addr = current_addr + 1

    if third_sec_addr > 0: 
        no_idea = read_int(data, current_addr, 1)
        current_addr = current_addr + 1
        while (data[current_addr] != 0):
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
            str_ = bytes(output).decode("cp932")
            strings2.append(str_.replace("\\", "\\\\"))

    functions = []

    current_addr = first_sec_addr
    ID_loc = 0 
   
    while (current_addr < second_sec_addr):
        ptr = read_int(data, current_addr, 2)
        if ptr not in result.locations_dict.keys():
            result.locations_dict[ptr] = "LOC_" + str(hex(ID_loc))
            ID_loc = ID_loc + 1

        result.locations.append(result.locations_dict[ptr])

        current_addr = current_addr + 2

    no_idea_bytes = []
    current_addr = second_sec_addr
    for i in range(0x10):
        no_idea_bytes.append(read_int(data, current_addr + i, 1))

    current_addr = current_addr + 0x10

    #functions.sort(key=lambda fun: fun.addr_start) 



    #for i_fun in range(0, len(functions)-1): 
    #    for i_fun_up in range(i_fun, len(functions)-1):
    #        if functions[i_fun].addr_start < functions[i_fun_up + 1].addr_start:
    #            functions[i_fun].addr_end = functions[i_fun_up + 1].addr_start
    #            break
            
    result.fun = function(current_addr, 0) 
    result.fun.addr_end = filesize
    #functions.sort(key=lambda fun: fun.ID) 

    result.fun.add_instructions(data)

    result.chip_ids = chip_ids
    result.functions = functions 
    result.no_idea_bytes = no_idea_bytes
    result.strings = strings
    result.strings2 = strings2
    result.no_idea = no_idea 
    return result

def to_py(ASF : ASFile):
    python_file = open(ASF.name + ".py", "wt",encoding='utf8')
    python_file.write("from ASCompiler import *\n\n")
    python_file.write("def script():\n")
    python_file.write("\n    set_script(\"" + ASF.name + "\")\n")
    python_file.write("\n    set_chips([")
    for id_in in range(len(ASF.chip_ids) - 1):
        python_file.write(hex(ASF.chip_ids[id_in]) + ", ")
    if (len(ASF.chip_ids) != 0):
        python_file.write(hex(ASF.chip_ids[len(ASF.chip_ids) - 1]))
    python_file.write("])\n")

    python_file.write("\n    set_strings([")
    for id_in in range(len(ASF.strings) - 1):
        python_file.write("\""+ASF.strings[id_in] + "\", ")
    if (len(ASF.strings) != 0):
        python_file.write("\""+ASF.strings[len(ASF.strings) - 1] + "\"") 
    python_file.write("])\n")

    if len(ASF.strings2) > 0:
        python_file.write("\n    set_strings2(" + str(hex(ASF.no_idea))+", [")
        for id_in in range(len(ASF.strings2) - 1):
            python_file.write("\""+ASF.strings2[id_in] + "\", ")
        if (len(ASF.strings2) != 0):
            python_file.write("\""+ASF.strings2[len(ASF.strings2) - 1] + "\"")
        python_file.write("])\n")


    python_file.write("\n    add_locations([")
    for id_in in range(len(ASF.locations) - 1):
        python_file.write("\"" +(ASF.locations[id_in]) + "\", ")
    if (len(ASF.no_idea_bytes) != 0):
        python_file.write( "\"" + ASF.locations[len(ASF.locations) - 1] + "\"")
    python_file.write("])\n")

    python_file.write("\n    set_mysterious_bytes([")
    for id_in in range(len(ASF.no_idea_bytes) - 1):
        python_file.write(hex(ASF.no_idea_bytes[id_in]) + ", ")
    if (len(ASF.no_idea_bytes) != 0):
        python_file.write(hex(ASF.no_idea_bytes[len(ASF.no_idea_bytes) - 1]))
    python_file.write("])\n")

    python_file.write("\n    #Code\n")
    
    python_file.write("#-------------------------------------------------#\n")
    python_file.write("# Original addresses " + hex(ASF.fun.addr_start) + " - " + hex(ASF.fun.addr_end) +"\n\n")
    python_file.write(ASF.fun.to_string(ASF.locations_dict))
        
    python_file.write("\n    assemble()")
    python_file.write("\n\nscript()")
    python_file.close()

