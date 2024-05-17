#
# this file describe the behavior of single exe unit with 1024 bit width and multi stage
# the alu name and id could be configured 
#
from src.base import *

class alu():
    """an alu has a inst_queue and alu pipeline"""
    """alu will check if the first instruction in queue has src ready"""
    """if so, alu will issue the oldest instruction to pipeline"""
    def __init__(self,inst:str,isq_len:int):
        """create single alu"""
        assert(inst in ['add','sub','mul','cmp','div','exp','pw2','mtf','bub'])
        self.inst = inst
        self.inst_queue = inst_queue(isq_len)
        self.pipeline = pipeline(CYC_DICT[f'{inst}'])
        pass

    def __str__(self) -> str:
        return f'{self.inst_queue}'
        
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
        if self.inst_queue.has_inst():
            peek_inst = self.inst_queue.peek_w()
            if peek_inst.src_chk(): #the first instruction could be executed for at least one stage
                poped_inst.issue()
                print(self)
                poped_inst = self.inst_queue.pop_w()
                finished_inst = self.pipeline.pop(poped_inst)
            else :
                finished_inst = self.pipeline.pop(instruction('bub'))
            if finished_inst.execute_done():
                return self.inst_queue.pop_i()
            else:
                return self.inst_queue.peek_i()
        else:
            pass

class exe():
    def __init__(self,topo_dict):
        """create the exe unit according to the topology dict"""
        self.topodict = {}
        for alu_key,alu_config in topo_dict.items():
            self.topodict[f'{alu_key}'] = [alu(alu_key,alu_config['isq'])] * alu_config['cnt']
        pass    

    def __str__(self) -> str:
        return f'{self.topodict}'
    
    def wakeup(self):
        vrf_list = []
        for alu_key,alu_list in self.topodict.items():
            for alu in alu_list:
                vrf_list.append(alu.wakeup())
        self.vrf.insert(vrf_list)
        return 0
    
    def get_free_list(self,alu_key:str) -> list:
        """get all free alu index for this alu key"""
        return [idx for idx,alu in enumerate(self.topodict[f'{alu_key}']) if alu.has_space()]

    def has_space(self,alu_key:str,alu_id:int):
        return self.topodict[f'{alu_key}'][alu_id].has_space()

    def insert(self,inst:instruction,alu_id:int):
        """public member function,for dispatch unit call to insert instruction(s)"""
        assert self.has_space(inst.get_inst(),alu_id)
        self.topodict[f'{inst.get_inst()}'][alu_id].insert(inst)
        pass

    def connect(self,vrf) -> None:
        """set dispatch connection"""
        self.vrf = vrf




        

    
