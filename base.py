cyc_dict = {
    'add':3,
    'sub':3,
    'mul':4,
    'cmp':2,
    'div':9,
    'exp':7,
    'pw2':6,
    'mtf':9,
    'bub':0
}

class instruction:
    """dataclass to track a instruction"""
    
    def __init__(self,inst:str,data_len:int=4,src = []):
        """construct the instruction dataclass with argv"""
        """len(argv) = 1: only setup inst"""
        """len(argv) > 1: setup inst & src"""
        assert(inst in ['add','sub','mul','cmp','div','exp','pw2','mtf','bub'])
        self.inst = inst
        self.datalength = data_len
        self.src_list = []
        self.finished_stage = 0
        self.issued_stage = 0
        self.pipedepth = cyc_dict[f'{self.inst}']

    def issue(self):
        """ """
        self.issued_stage += 1
        assert(self.issued_stage < self.datalength)
        return self.log()

    def finish(self):
        """ """
        self.finished_stage += 1
        assert(self.finished_stage < self.issued_stage)
        return self.log()
    
    def is_bub(self):
        """check if this instruction was a bulb,if so return true"""
        return self.inst == 'bub'
    
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

    def log(self):
        """return current stage"""

        return f'{self.inst}:{self.id:3}*{self.datalength};\
                src:{self.src1:3}.{self.src2:3};\
                wb:{self.finished_stage};issue:{self.issued_stage}'
    

class simple_inst_queue():
    def __init__(self, depth: int):
        self.queue = [instruction('bub')] * depth
        return 0
    
    def __str__(self):
        return self.queue

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
        self.queue = []

    def has_space(self):
        return len(self.queue) < self.depth

    def insert(self,inst: instruction) :
        """insert the inst_id to last empty slot ret non zero: successfully insert"""
        assert self.has_space()
        self.queue.append(inst)

    def pop(self):
        """pop the first instruction and return"""
        return self.queue.pop(0)

    def peek(self):
        """peek the last instruction"""
        return self.queue[0]
    
