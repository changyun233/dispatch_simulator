from src.base import *

class vrf():
    def __init__(self) -> None:
        self.reg_inst_list = []

    def wakeup(self):
        for single_inst in self.reg_inst_list:
            single_inst.reg()
        self.reg_inst_list = []

    def insert(self,inst_list:list):
        self.reg_inst_list = inst_list
        