from src.base.base import *
from src.base.instruction import instruction

class simple_inst_queue():
    def __init__(self, depth: int):
        self.queue = [instruction('bub')] * depth
    
    def __str__(self):
        ret_str = ''
        for inst in self.queue:
            ret_str = ret_str+f'{inst.get_addr():0>3d} '
        return ret_str[:-1]

class pipeline(simple_inst_queue):
    """alu pipeline"""
    """much more like a score board to recored instruction state"""
    def pop(self,inst:instruction = instruction('bub')) -> instruction :
        """pass the data to next pipeline stage """
        """return the retire instruction id"""
        self.queue.insert(0,inst)
        return self.queue.pop()
    
class inst_queue(simple_inst_queue):
    """ instruction queue to be executed by alu"""    
    def __init__(self, depth: int):
        self.waiting_queue = []
        self.issued_queue = []
        self.depth = depth

    def get_remain(self) -> int:
        return self.depth - len(self.waiting_queue) - len(self.issued_queue)

    def is_empty(self):
        return (len(self.waiting_queue) + len(self.issued_queue)) == 0

    def has_space(self):
        return (len(self.waiting_queue) + len(self.issued_queue)) < self.depth
    
    def need_issue(self):
        return len(self.waiting_queue) > 0
    
    def can_issue(self) -> bool:
        if self.need_issue():
            return self.waiting_queue[0].src_chk()
        else:
            return False

    def peek_w(self):
        return self.waiting_queue[0]
    
    def issue(self):
        ret_inst = self.waiting_queue[0]
        ret_inst.issue()
        if ret_inst.issue_done():
            self.issued_queue.append(self.waiting_queue.pop(0))
        return ret_inst
    
    def pop_exed(self):
        if len(self.issued_queue) > 0:
            if self.issued_queue[0].execute_done():
                self.issued_queue.pop(0)

    def pop_in(self,inst:instruction):
        """insert a instruction to newest position"""
        assert(self.has_space())
        self.waiting_queue.append(inst)

    def __str__(self):
        ret_str = ''
        for inst in self.waiting_queue:
            ret_str = ret_str+f'{inst.get_addr():0>3d} '
        ret_str +=': ' 
        for inst in self.issued_queue:
            ret_str = ret_str+f'{inst.get_addr():0>3d} '
        return ret_str[:-1]