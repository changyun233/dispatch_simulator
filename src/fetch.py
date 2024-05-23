#
# this file describes a instruction fetch unit combined with decode function.
# simply read instruction from file
#

from src.base.all import *
import src
import json


def line_parser(inst_line:str) -> instruction:
    """parse a line into instruction """
    str_list = inst_line.split(' ')
    addr = int(str_list[0])
    cmd = str_list[1]
    data_len = int(str_list[2])
    src_list = json.loads(str_list[3])
    inst_return = instruction(cmd,addr,data_len)
    return (inst_return,src_list) 

def file_parser(file_in:str) -> list:
    return_list = [instruction('bub')]
    with open(file_in,'r') as f:
        for line in f.readlines()[1:]:
            parsed_inst,src_list = line_parser(line)
            parsed_inst.set_src([return_list[i]for i in src_list])
            return_list.append(parsed_inst)
    return_list.pop(0)
    return return_list

class fetch(clocked_object):
    def __init__(self,inst_file) -> None:
        super().__init__('fetch')
        self.inst_list = file_parser(inst_file)
        self.dispatch_U = 0
        self.dispatch_full = False

    def log(self) -> dict:
        return {f'{self._name}':str(self)}

    def wakeup(self) -> None :
        """pop out a instruction if dispatch has space"""
        if(self.dispatch_U.has_space() and not self.is_free()):
            self.dispatch_U.insert(self.inst_list.pop(0))
        else:
            self.dispatch_U.insert(instruction('bub'))
            self.dispatch_full = True

    def ft_dp_full(self) -> bool:
        return self.dispatch_full

    def connect(self,disp_u:clocked_object) -> None:
        """set dispatch connection"""
        assert(disp_u.get_name)
        self.dispatch_U = disp_u

    def is_free(self) -> bool:
        """if the fetch unit has sent all instructions"""
        return len(self.inst_list) == 0
    
    def insert(self,inst:instruction):
        self.inst_list.append(inst)

    def __str__(self):
        ret_str = ''
        for inst in self.inst_list:
            ret_str = ret_str+f'{inst.get_addr():0>3d} '
        return ret_str[:-1]



        