from src.base.base import *

class instruction(regular_object):
    """dataclass to track a instruction"""
    
    def __init__(self,inst:str,addr:int = 0, data_len:int=4,tar:int = -1,src:list  = []):
        """construct the instruction dataclass with argv"""
        """len(argv) = 1: only setup inst"""
        """len(argv) = 2: setup inst & src"""
        """len(argv) = 3: setup inst & src & dispatchTarget"""
        assert(inst in INSTRUCTIONS)
        self.inst = inst
        self.addr = addr
        self.datalength = data_len
        self.src_list = src
        self.finished_stage = 0
        self.issued_stage = 0
        self.pipedepth = CYC_DICT[f'{self.inst}']
        self.dispatch_target = tar

    def __str__(self):
        return f'{self.addr:3}{self.inst}*{self.datalength} R:{self.finished_stage} I:{self.issued_stage} S:{self.get_src_id()}'

    def get_addr_s(self):
        """public function,get addr of this instruction, for debug"""
        return f'{self.addr:0>3d}'
    
    def get_addr(self):
        """public function,get addr of this instruction, for debug"""
        return self.addr

    def issue(self):
        """ """
        self.issued_stage += 1
        assert(self.issued_stage <= self.datalength)

    def reg(self):
        """ """
        self.finished_stage += 1
        assert(self.finished_stage <= self.issued_stage)
    
    def is_bub(self):
        """check if this instruction was a bulb,if so return true"""
        return self.inst == 'bub'
    
    def get_inst(self):
        return self.inst
    
    def issue_done(self):
        """check if the instruction nolonger need to be stalled in waiting queue"""
        return self.issued_stage == self.datalength
    
    def execute_done(self):
        """check if the instruction nolonger need to be stalled in instruction queue"""
        return self.finished_stage == self.datalength

    def dep_chk(self,issue_cnt):
        """issue_cnt:instruction which depends on this one instruction has been issued for issure_cnt times"""
        """return whether the finished stage > issue_cnt"""
        return issue_cnt < self.finished_stage
    
    def src_chk(self): 
        """check whether the src instruction has finished"""
        """if all pass return true"""
        chk_list = []
        for src_inst in self.src_list:
            chk_list.append(src_inst.dep_chk(self.issued_stage))
        return False not in chk_list
    
    def set_src(self,inst_list:list) :
        self.src_list = inst_list

    def get_src_id(self):
        return [inst.get_addr() for inst in self.src_list]
        

    def get_dispatch_target(self):
        return self.dispatch_target
