from config.config_file import *

class instruction:
    """dataclass to track a instruction"""
    
    def __init__(self,inst:str,addr:int = 0, data_len:int=4,src:list  = []):
        """construct the instruction dataclass with argv"""
        """len(argv) = 1: only setup inst"""
        """len(argv) > 1: setup inst & src"""
        assert(inst in INSTRUCTIONS)
        self.inst = inst
        self.addr = addr
        self.datalength = data_len
        self.src_list = src
        self.finished_stage = 0
        self.issued_stage = 0
        self.pipedepth = CYC_DICT[f'{self.inst}']

    def __str__(self):
        return f'{self.inst}-{self.addr:0>3d}'

    def addr(self):
        """public function,get addr of this instruction, for debug"""
        return self.addr

    def issue(self):
        """ """
        self.issued_stage += 1
        assert(self.issued_stage < self.datalength)
        return self.log()

    def reg(self):
        """ """
        self.finished_stage += 1
        assert(self.finished_stage <= self.issued_stage)
        return self.log()
    
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
        return self

    def log(self):
        """return current stage"""

        return f'{self.inst}:{self.id:3}*{self.datalength};\
                src:{self.src1:3}.{self.src2:3};\
                reg:{self.finished_stage};issue:{self.issued_stage}'
    

class simple_inst_queue():
    def __init__(self, depth: int):
        self.queue = [instruction('bub')] * depth
    
    def __str__(self):
        ret_str = ''
        for inst in self.queue:
            ret_str = ret_str+f'{inst.addr():0>3d},'
        return ret_str[:-1]

class pipeline(simple_inst_queue):
    """alu pipeline"""
    """much more like a score board to recored instruction state"""
    def pop(self,inst:instruction = instruction('bub')) -> instruction :
        """pass the data to next pipeline stage """
        """return the retire instruction id"""
        self.queue.insert(0,inst)
        return self.queue.pop()
    
class inst_queue():
    """ instruction queue to be executed by alu"""    
    def __init__(self, depth: int):
        self.depth = depth
        self.waiting_queue = []
        self.issued_queue = []

    def has_space(self):
        return (len(self.waiting_queue) + len(self.issued_queue)) < self.depth
    
    def has_inst(self):
        return (len(self.waiting_queue) + len(self.issued_queue)) > 0

    def pop_in(self,inst: instruction) :
        """insert the inst_id to last empty slot ret non zero: successfully insert"""
        assert self.has_space()
        self.waiting_queue.append(inst)

    def issue_done(self):
        assert self.waiting_queue[0].issue_done()
        self.issued_queue.append(self.waiting_queue.pop(0))

    def pop_w(self):
        """pop the first instruction and return"""
        last_inst = self.peek_w()
        if last_inst.issue_done():
            self.issue_done()
            return last_inst
        else:
            return self.waiting_queue.pop(0)
    
    def peek_w(self):
        """peek the last instruction"""
        return self.waiting_queue[0]
    
    def pop_i(self):
        """pop the first instruction and return"""
        return self.issued_queue.pop(0)

    def peek_i(self):
        """peek the last instruction"""
        return self.issued_queue[0]
    
