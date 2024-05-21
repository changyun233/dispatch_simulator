from src.base.all import *
import pandas as pd
import os

class scroop(clocked_object):
    """class to record object states"""
    def __init__(self) -> None:
        super().__init__('_pmu')
        self.name_list = []
        self.components = []
        self.log_dfs = []
        self.alu_dfs = pd.DataFrame()
        self.path = f'logs/'
        os.makedirs(f'{self.path}',exist_ok=True)

    def __str__(self):
        return self.components.__str__()
    
    def wakeup(self,cycle:int):
        for i in range(len(self.name_list)):
            data = pd.DataFrame(self.components[i].log(),index = [cycle])
            self.log_dfs[i] = pd.concat([self.log_dfs[i],data])
            if self.components[i].get_name() == 'exe':
                data = pd.DataFrame(self.components[i].logq(),index = [cycle])
                self.alu_dfs = pd.concat([self.alu_dfs,data])
        

    
    def connect(self,component:clocked_object):
        self.name_list.append(component.get_name())
        self.components.append(component)
        self.log_dfs.append(pd.DataFrame())

    def insert(self):
        for i in range(len(self.name_list)):
            file_path = f'{self.path}{self.name_list[i]}.csv'
            self.log_dfs[i].to_csv(file_path)
        self.alu_dfs.to_csv(f'{self.path}aluQueue.csv')
        pass
