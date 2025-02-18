from config.config_file import *

from src.fetch import fetch
from src.dispatch import dispatch
from src.exe import exe
from src.vrf import vrf
from src.scroop import scroop
from src.recorder import recorder
#from src.dispatch import *

class core():
    """core top module"""
    def __init__(self,argv_list) -> None:
        """argv_list:[inst_file,arb_method]"""

        self.fetch_U = fetch(argv_list[0])
        self.dispatch_U = dispatch(argv_list[1])
        self.exe_U = exe(EXE_CONFIG)
        self.vrf_U = vrf()
        self.scroop_U = scroop()
        self.recorder_U = recorder()

        self.fetch_U.connect(self.dispatch_U)
        self.dispatch_U.connect(self.fetch_U)
        self.dispatch_U.connect(self.exe_U)
        self.exe_U.connect(self.vrf_U)

        
        self.scroop_U.connect(self.fetch_U)
        self.scroop_U.connect(self.dispatch_U)
        self.scroop_U.connect(self.exe_U)
        self.scroop_U.connect(self.vrf_U)

        self.recorder_U.connect(self.fetch_U)
        pass

    def wakeup(self,cycle:int) -> None:
        self.vrf_U.wakeup()
        self.exe_U.wakeup()
        self.dispatch_U.wakeup()
        self.fetch_U.wakeup()
        self.scroop_U.wakeup(cycle)
        self.recorder_U.wakeup(cycle)
        pass

    def start_execution(self) -> None:
        self.exe_U.start_execution()

    def issue_full(self) -> bool:
        return self.fetch_U.ft_dp_full()
    
    def fetch_empty(self) -> bool:
        return self.fetch_U.is_free()
    
    def issue_done(self) -> bool:
        return self.exe_U.is_empty()
