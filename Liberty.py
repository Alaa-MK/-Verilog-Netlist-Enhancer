from liberty.parser import parse_liberty
from liberty.types import select_timing_table
import re

class Liberty:
    def __init__(self):
        self.library = parse_liberty(open("osu035.lib").read())
    
    def _interpolate(self, x1,x2,y1,y2,c):
        return y1 + (y2-y1)*(c-x1)/(x2-x1)
    
    def get_capacitance(self, cell_name, pin_name):
        cell = self.library.get_group('cell', cell_name)
        assert cell is not None
        pin = cell.get_group('pin', pin_name)   
        capacitance = float(re.search('capacitance:(.*?);',str(pin))[0][13:-1])
        return capacitance
    
    def get_delay_time(self, cell_name, pin_name, out_cap):
        cell = self.library.get_group('cell', cell_name)
        assert cell is not None
        pin = cell.get_group('pin', 'Y') 
        time_table= select_timing_table(pin,pin_name,'rise_transition')
        index=time_table.get_array('values')
        if out_cap==0.06:
            delay= index[0][0]
        elif out_cap==0.18:
            delay= index[0][1]
        elif out_cap==0.42:
            delay= index[0][2]
        elif out_cap==0.6:
            delay= index[0][3]
        elif out_cap==1.2:
            delay= index[0][4]
        elif out_cap > 0.06 and out_cap < 0.18:
            delay = self.interpolate(0.06,0.18,index[0][0], index[0][1],out_cap)
        elif out_cap > 0.18 and out_cap < 0.42:
            delay = self.interpolate(0.18,0.42,index[0][1], index[0][2],out_cap)
        elif out_cap > 0.42 and out_cap < 0.6:
            delay = self.interpolate(0.42,0.6,index[0][2], index[0][3],out_cap)
        elif out_cap > 0.6 and out_cap < 1.2:
            delay = self.interpolate(0.6,1.2,index[0][3], index[0][4],out_cap)
        elif out_cap < 0.6:
            delay = self.interpolate(0.6,1.2,index[0][0],index[0][1],out_cap)
        elif out_cap > 1.2:
            delay = self.interpolate(0.6,1.2,index[0][3],index[0][4],out_cap)
        return delay