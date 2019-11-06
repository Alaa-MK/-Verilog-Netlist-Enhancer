from liberty.parser import parse_liberty
from liberty.types import select_timing_table
from sklearn import linear_model
import numpy as np

library = parse_liberty(open("osu035.lib").read())

def interpolate(x1,x2,y1,y2,c):
    return y1 + (y2-y1)*(c-x1)/(x2-x1)

def get_capacitance(cell_name,pin_name):
    cell = library.get_group('cell', cell_name)
    assert cell is not None
    pin = cell.get_group('pin', pin_name)   
    capacitance = float(re.search('capacitance:(.*?);',str(pin))[0][13:-1])
    return capacitance

def get_delay_time(cell_name,pin_name,c):
    cell = library.get_group('cell', cell_name)
    assert cell is not None
    pin = cell.get_group('pin', 'Y') 
    time_table= select_timing_table(pin,pin_name,'rise_transition')
    index=time_table.get_array('values')
    if c==0.06:
        delay= index[0][0]
    elif c==0.18:
        delay= index[0][1]
    elif c==0.42:
        delay= index[0][2]
    elif c==0.6:
        delay= index[0][3]
    elif c==1.2:
        delay= index[0][4]
    elif c > 0.06 and c < 0.18:
        delay = interpolate(0.06,0.18,index[0][0], index[0][1],c)
    elif c > 0.18 and c < 0.42:
        delay = interpolate(0.18,0.42,index[0][1], index[0][2],c)
    elif c > 0.42 and c < 0.6:
        delay = interpolate(0.42,0.6,index[0][2], index[0][3],c)
    elif c > 0.6 and c < 1.2:
        delay = interpolate(0.6,1.2,index[0][3], index[0][4],c)
    elif c < 0.6:
        delay = interpolate(0.6,1.2,index[0][0],index[0][1],c)
    elif c > 1.2:
        delay = interpolate(0.6,1.2,index[0][3],index[0][4],c)
    return delay
        

"""
def main():
    print(get_delay_time("AND2X1",'A',0.42))

if __name__=="__main__":
    main()
"""
