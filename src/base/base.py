from __future__ import annotations
from config.config_file import *
from abc import ABC, abstractmethod

    
class regular_object(ABC):
    """a base class to setup non clocked objects"""
    _name = ""
    _id = 0
    def __init__(self,name_str:str,id_int:int=0) -> None:
        self._name = name_str
        self._id = id_int
    
    def get_name(self):
        return self._name
    
    def get_id(self):
        return self._id
    
    def full_name(self):
        return f'{self._name}{self._id}'
    
    @abstractmethod
    def __str__(self):
        pass

class clocked_object(regular_object):
    """a base class to set up all objects"""

    @abstractmethod
    def wakeup(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def connect(self,another_comp:clocked_object):
        pass


