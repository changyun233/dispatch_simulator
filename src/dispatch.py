#
# this file describe a simple dispatch unit to perfrom fecth, decode and dispatch to exe unit 
# 

import pandas as pd
from src.base import *

class dispatch():
    def __init__(self,arb_method) -> None:
        self.dispatch_slot = []
        self.br_cnt = 0
        self.rr_ptr = 0
        pass


    def wakeup(self) -> int:
        if len(self.dispatch_slot) < 1: #noinstruction was decoded
            return 0
        if self.dispatch_slot[0].is_bub(): # get a bub slot
            return 0
        else: # a valid instruction
            alu_id = self.in_order_arb(self.dispatch_slot[0])
            if alu_id == -1: # no alu space
                return 0
            else:
                self.exe_U.insert(self.dispatch_slot.pop(),alu_id)
                return 0
            
    def top_arb(self,method, inst: instruction ) -> int:
        arb_sel = {
            'glb_rr':self.glb_rr_arb,
            'loc_rr':self.local_rr_arb,
            'glb_bq':self.glb_brq_arb,
            'loc_bq':self.local_brq_arb,
            'inorde':self.in_order_arb
        }
        try:
            function = arb_sel[method]
            return function(inst)
        except KeyError:
            raise ValueError('invald arb method')
            return 0
    
    def glb_rr_arb(self,inst: instruction) -> int:
        """all instruction share a rr reg"""
        return -1
    
    def local_rr_arb(self,inst: instruction) -> int:
        """each instruction has its own rr reg"""
        return -1
    
    def glb_brq_arb(self,inst: instruction) -> int:
        """all instruction share a rr reg"""
        return -1
    
    def local_brq_arb(self,inst: instruction) -> int:
        """each instruction has its own rr reg"""
        return -1

    def in_order_arb(self,inst: instruction) -> int:
        """if 1st alu has free space,insert into 1st"""
        freelist = self.exe_U.get_free_list()
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

    
    def connect_f(self,fet_u) -> None:
        """set dispatch connection"""
        self.fetch_U = fet_u

    def connect_e(self,exe_U) -> None:
        """set dispatch connection"""
        self.exe_U = exe_U
    
    

