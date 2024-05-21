from src.base.all import *
from src.base.base import clocked_object

class vrf(clocked_object):
    def __init__(self) -> None:
        super().__init__('vrf')
        self.reg_inst_list = []

    def __str__(self):
        ret_str = ''
        for inst in self.reg_inst_list:
            ret_str = ret_str+f'{inst.get_addr():0>3d} '
        return ret_str[:-1]
    
    def connect(self, another_comp: clocked_object):
        raise SyntaxError('vrf do not need any connect')

    def wakeup(self):
        for single_inst in self.reg_inst_list:
            if not single_inst.is_bub():
                single_inst.reg()
        self.reg_inst_list = []

    def insert(self,inst_list:list):
        self.reg_inst_list = [inst for inst in inst_list if not inst.is_bub()]

    def log(self) -> dict:
        return {f'{self._name}':str(self)}
        