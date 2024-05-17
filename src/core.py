from config.config_file import *

from src.fetch import fetch
from src.dispatch import dispatch
from src.exe import exe
from src.vrf import vrf
#from src.dispatch import *

class core():
    """core top module"""
    def __init__(self,argv_list) -> None:
        """argv_list:[inst_file,arb_method]"""

        self.fetch_U = fetch(argv_list[0])
        self.dispatch_U = dispatch(argv_list[1])
        self.exe_U = exe(EXE_CONFIG)
        self.vrf_U = vrf()

        self.fetch_U.connect(self.dispatch_U)
        self.dispatch_U.connect_f(self.fetch_U)
        self.dispatch_U.connect_e(self.exe_U)
        self.exe_U.connect(self.vrf_U)
        pass

    def wakeup(self) -> None:
        self.vrf_U.wakeup()
        self.exe_U.wakeup()
        self.dispatch_U.wakeup()
        self.fetch_U.wakeup()
        pass
