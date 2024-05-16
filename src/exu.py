#
# this file describe the behavior of single exe unit with 1024 bit width and multi stage
# the alu name and id could be configured 
#
from src.base import *
from config.config_file import *

class exu():
    def __init__(self,topo_dict):
        """create the exe unit according to the topology dict"""
        self.topodict = {}
        for alu_key,alu_config in topo_dict.items():
            self.topodict[f'{alu_key}'] = [alu(alu_config['isq'])] * alu_config['cnt']
        pass    

    def __str__(self) -> str:
        return f'{self.topodict}'

    def has_space(self,alu_key:str,alu_id:int):
        return self.topodict[f'{alu_key}'][alu_id].has_space()

    def load_inst(self,inst:instruction,alu_id:int):
        assert self.has_space(inst.get_inst(),alu_id)
        self.topodict[f'{inst.get_inst()}'][alu_id].insert(inst)
        pass



class alu():
    """an alu has a inst_queue and alu pipeline"""
    """alu will check if the first instruction in queue has src ready"""
    """if so alu will issue the instruction to pipeline"""
    def __init__(self,inst:str,isq_len:int):
        """create single alu"""
        assert(inst in ['add','sub','mul','cmp','div','exp','pw2','mtf','bub'])
        self.inst = inst
        self.inst_queue = inst_queue(isq_len)
        self.pipeline = pipeline(CYC_DICT[f'{inst}'])
        
    def has_space(self):
        """whether this alu cmd queue has room for new one"""
        return self.inst_queue.has_space()
    
    def insert(self,inst: instruction):
        """insert new instruction """
        assert inst == self.inst
        self.inst_queue.insert(inst)
    
    def wakeup(self):
        """execute pipeline refresh,return a valid instruction if alu successfully piped a stage"""
        finished_inst = 0
        peek_inst = self.inst_queue.peek_w()

        if peek_inst.src_chk(): #the first instruction could be executed for at least one stage
            poped_inst.issue()
            poped_inst = self.inst_queue.pop_w()
            finished_inst = self.pipeline.pop(poped_inst)
        else :
            finished_inst = self.pipeline.pop(instruction('bub'))
        if not finished_inst.is_bub():
            finished_inst.finish()
            if finished_inst.execute_done():
                self.inst_queue.pop_i()

    
