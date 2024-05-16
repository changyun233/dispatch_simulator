import numpy as np
import sys
import pandas as pd
from pandas import Series,DataFrame

#inst_id,retire_tick

"""
LSU	5
ADD	3
SUB	3
MUL	4
DIV	9
CMP	2
EXP	7
POW2	6
MULTIF	9
"""

tick = 0
pc = 0
        

def arb_free(inst,alu_dict,br_cnt):
    """return the free ALU id according to the inst"""
    global tick
    ist_dict = alu_dict[f'{inst}']
    for key,sub_dict in zip(ist_dict.keys(),ist_dict.values()) :
        if tick > int(sub_dict['retire_tick']):
            return int(key)
    return -1

def main(argv):
    """main function of simulator,act like a top module"""
    global pc
    global tick
    br_cnt = 0
    
    alu_dict = {
        'add':{ '0':{'retire_tick':0,
                     'inst_id':0},
                '1':{'retire_tick':0,
                     'inst_id':0},},
        'sub':{ '0':{'retire_tick':0,
                     'inst_id':0},
                '1':{'retire_tick':0,
                     'inst_id':0},},
        'mul':{ '0':{'retire_tick':0,
                     'inst_id':0},
                '1':{'retire_tick':0,
                     'inst_id':0},},
        'cmp':{ '0':{'retire_tick':0,
                     'inst_id':0},
                '1':{'retire_tick':0,
                     'inst_id':0},},
        'div':{ '0':{'retire_tick':0,
                     'inst_id':0},},
        'exp':{ '0':{'retire_tick':0,
                     'inst_id':0},},
        'pw2':{ '0':{'retire_tick':0,
                     'inst_id':0},},
        'mtf':{ '0':{'retire_tick':0,
                     'inst_id':0},},
    }

    cyc_dict = {
        'add':3,
        'sub':3,
        'mul':4,
        'cmp':2,
        'div':9,
        'exp':7,
        'pw2':6,
        'mtf':9,
    }

    df = pd.read_csv(argv[0])

    log_df = pd.DataFrame(alu_dict)

    while True:
        """fetch instruction from file"""
        if pc >= len(df):
            print(f'dispatch done @ {tick} tick')
            break
        elif df.iat[pc,1] == 'beq':
            br_cnt += 1
            pc += 1
            tick += 1
        elif df.iat[pc,1] == 'reg':
            pc +=1
            tick += 1
        else:
            tick += 1
            alu_id = arb_free(df.iat[pc,1],alu_dict,br_cnt)
            if alu_id != -1 : #has free alu for current inst.
                alu_dict[f'{df.iat[pc,1]}'][f'{alu_id}']['retire_tick'] = tick + \
                            cyc_dict[f'{df.iat[pc,1]}']
                print(f'{df.iat[pc,1]}{alu_id} exi {pc} @ tick {tick}')
                pc += 1
            else:
                print(f'{df.iat[pc,1]} busy @ tick {tick}')

            log_df = pd.concat([log_df,pd.DataFrame(alu_dict)])
    log_df.to_csv('log.csv')


            
        

        
    

if __name__ == "__main__":
    main(sys.argv[1:])
