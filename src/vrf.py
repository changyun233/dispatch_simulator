from src.base import *

class vrf():
    def __init__(self) -> None:
        self.wb_inst_list = []

    def wakeup(self):
        for sing_inst in self.wb_inst_list:
            sing_inst.wb()
        self.wb_inst_list = []

    def writeback(self,inst_list:lsit):
        self.wb_inst_list = inst_list