#
# this file describe a simple dispatch unit to perfrom fecth, decode and dispatch to exe unit 
# 

import pandas as pd
from src.base.all import *

class dispatch(clocked_object):
    def __init__(self,arb_method) -> None:
        super().__init__('dispatch')
        self.dispatch_slot = []
        self.rr_ptr = True
        self.arb_methord = arb_method
        pass

    def log(self) -> dict:
        return {f'{self._name}':str(self)}


    def wakeup(self) -> None:
        if len(self.dispatch_slot) < 1: #noinstruction was decoded
            pass
        else: # a valid instruction
            alu_id = self.top_arb(self.dispatch_slot[0])
            print(f'{self.dispatch_slot[0].get_addr()}issued to {self.dispatch_slot[0].get_inst()}{alu_id}')
            if alu_id == -1: # no alu space
                pass
            else:
                self.exe_U.insert(self.dispatch_slot.pop(),alu_id)
        pass
            
    def top_arb(self, inst: instruction ) -> int:
        arb_sel = {
            'global_rr':self.glb_rr_arb,
            'inorder':self.in_order_arb,
            'balance':self.load_blc_arb
        }
        try:
            function = arb_sel[self.arb_methord]
            return function(inst)
        except KeyError:
            raise ValueError('invald arb method')
    
    def load_blc_arb(self,inst: instruction) -> int:
        """all instruction share a rr reg"""
        remain_list = self.exe_U.get_remain_list(inst.get_inst())
        max_remain = max(remain_list)
        if max_remain == 0:
            return -1
        else:
            return remain_list.index(max(remain_list))
    
    def glb_rr_arb(self,inst: instruction) -> int:
        """all instruction share a rr reg"""
        freelist = self.exe_U.get_free_list(inst.get_inst())
        if len(freelist) < 1:
            return -1
        elif len(freelist) == 1 :
            return freelist[0]
        else :
            self.rr_ptr = not self.rr_ptr
            return freelist[self.rr_ptr]
    
    def in_order_arb(self,inst: instruction) -> int:
        """if 1st alu has free space,insert into 1st"""
        freelist = self.exe_U.get_free_list(inst.get_inst())
        if len(freelist) < 1:
            return -1
        else:
            return freelist[0]
    
    
    def has_space(self) -> bool:
        """back pressure for instruction fetch"""
        return len(self.dispatch_slot) < 1
    
    def insert(self,inst:instruction) -> None:
        """insert instruction to dispatch slot"""
        if inst.is_bub():
            assert(self.fetch_U.is_free() or not self.has_space())
        else:
            self.dispatch_slot.append(inst)
        assert len(self.dispatch_slot) <= 1

    
    def connect(self,comp_U:clocked_object) -> None:
        """set dispatch connection"""
        if comp_U.get_name() == 'fetch':
            self.fetch_U = comp_U
        elif comp_U.get_name() == 'exe':
            self.exe_U = comp_U
        else:
            raise ValueError('unknown unit')

    def __str__(self):
        if len(self.dispatch_slot) > 0:
            return f'{self.dispatch_slot[0]}'
        else:
            return '000'
    
    

