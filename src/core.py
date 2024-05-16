from config.config_file import *
import src
import src.exu
import src.fetch
import src.vrf
#from src.dispatch import *

class core():
    def __init__(self,argv_list) -> None:
            self.fetch = src.fetch()
            self.dispatch = src.dispatch()
            self.exu = src.exu()
            self.vrf = src.vrf()



        pass

    