from src.base.all import *
import pandas as pd
import os

class recorder(clocked_object):
    """class to record object states"""
    def __init__(self) -> None:
        super().__init__('_imu')
        self.inst_list = []
        self.log_df = pd.DataFrame()
        self.path = f'logs/'
        os.makedirs(f'{self.path}',exist_ok=True)

    def __str__(self):
        return self.components.__str__()
    
    def wakeup(self,cycle:int):
        log_dict = {}
        for i in range(len(self.inst_list)):
            log_dict[str(self.inst_list[i])[:5]] = str(self.inst_list[i])[6:]
        data = pd.DataFrame(log_dict,index = [cycle])
        self.log_df = pd.concat([self.log_df,data])
    
    def connect(self,component:clocked_object):
        assert(component.get_name() == 'fetch')
        self.inst_list = component.inst_list.copy()

    def insert(self):
        file_path = f'{self.path}inst.csv'
        self.log_df.to_csv(file_path)
        pass
