#
# this file describe the behavior of single exe unit with 1024 bit width and multi stage
# the alu name and id could be configured 
#
from config.config_file import *
from src.base.all import *

class alu():
    """an alu has a inst_queue and alu pipeline"""
    """alu will check if the first instruction in queue has src ready"""
    """if so, alu will issue the oldest instruction to pipeline"""
    def __init__(self,inst:str,isq_len:int):
        """create single alu"""
        assert(inst in INSTRUCTIONS)
        self.inst = inst
        self.inst_queue = inst_queue(isq_len)
        self.pipeline = pipeline(CYC_DICT[f'{inst}'])
        pass

    def __str__(self) -> str:
        return f'{self.pipeline}'
    
    def logq(self) -> str:
        return str(self.inst_queue)
        
    def has_space(self):
        """whether this alu cmd queue has room for new one"""
        return self.inst_queue.has_space()
    
    def insert(self,inst: instruction):
        """insert new instruction """
        assert inst.get_inst() == self.inst
        self.inst_queue.pop_in(inst)

    def issue_allowed(self) -> bool:
        """check if the last inst in waiting Queue was able to poped into pipeline"""
        if self.inst_queue.has_inst():
            return self.inst_queue.peek_w().src_chk()
        else:
            return False
        
    def pop_issued_inst(self) -> None:
        if self.inst_queue.has_inst():
            if self.inst_queue.issue_done():
                self.inst_queue.issue_done()
        
    def pop_finished_inst(self) -> None:
        if self.inst_queue.i_has_inst():
            if self.inst_queue.peek_i().execute_done():
                self.inst_queue.pop_i()
    
    def wakeup(self):
        """execute pipeline refresh,return a valid instruction if alu successfully piped a stage"""
        
        #select a inst from inst_queue
        self.inst_queue.pop_exed()

        if self.inst_queue.can_issue():
            return self.pipeline.pop(self.inst_queue.issue())
        else:
            return self.pipeline.pop(instruction('bub'))


class exe(clocked_object):
    def __init__(self,topo_dict):
        """create the exe unit according to the topology dict"""
        super().__init__('exe')
        self.topodict = {}
        for alu_key,alu_config in topo_dict.items():
            alu_list = [alu(alu_key,alu_config['isq']) for i in range(alu_config['cnt'])]
            self.topodict[f'{alu_key}'] = alu_list
        pass

    def __str__(self) -> str:
        return f'{self.topodict}'
    
    def log(self) -> dict:
        ret_dict = {}
        for alu_key,alu_list in self.topodict.items():
            for alu_id,alu in enumerate(alu_list):
                ret_dict[f'{alu_key}{alu_id}'] = str(alu)
        return ret_dict
    
    def logq(self) -> dict:
        ret_dict = {}
        for alu_key,alu_list in self.topodict.items():
            for alu_id,alu in enumerate(alu_list):
                ret_dict[f'{alu_key}{alu_id}'] = alu.logq()
        return ret_dict

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

    def connect(self,vrf:clocked_object) -> None:
        """set dispatch connection"""
        self.vrf = vrf




    
