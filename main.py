from config.config_file import *
from src.core import core
import sys

def main(argv):
    core_U = core(argv)

    for i in range(60):
        core_U.wakeup(i)

    core_U.scroop_U.insert()
    core_U.recorder_U.insert()

if __name__=="__main__":
    main(sys.argv[1:])