from config.config_file import *
from src.core import core
import sys

def main(argv):
    core_U = core(argv)
    i = 0 
    issue_done_cnt = 0

    while True:
        i += 1
        core_U.wakeup(i)

        if core_U.fetch_empty() or core_U.issue_full():
            print(f'execution start @ cycle{i}')
            core_U.start_execution()
            break
    
    while True:
        i += 1
        core_U.wakeup(i)
        if core_U.issue_done():
            issue_done_cnt += 1
            if issue_done_cnt == 20:
                print(f'issue done @ cycle{i-20}')
                break
            
    core_U.scroop_U.insert()
    core_U.recorder_U.insert()

if __name__=="__main__":
    main(sys.argv[1:])