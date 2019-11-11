from liberty.parser import parse_liberty
from liberty.types import select_timing_table
import re

class Liberty:
    def __init__(self, filename):
        self.library = parse_liberty(open(filename).read())
    
    def _interpolate(self, x1,x2,y1,y2,c):
        return y1 + (y2-y1)*(c-x1)/(x2-x1)

    def get_middle_capacitance(self):
        cell = self.library.get_group('cell', 'AND2X1')
        pin = cell.get_group('pin', 'Y')
        time_table= select_timing_table(pin,'A','rise_transition')
        index2=time_table.get_array('index_2')
        return index2[0][2]
    
    def get_pin_capacitance(self, cell_name, pin_name):
        cell = self.library.get_group('cell', cell_name)
        assert cell is not None
        pin = cell.get_group('pin', pin_name)  
        capacitance = float(re.search('capacitance:(.*?);',str(pin))[0][13:-1])
        return capacitance
    
    def get_pin_delay(self, cell_name, pin_name, out_cap):
        cell = self.library.get_group('cell', cell_name)
        assert cell is not None
        if cell_name[0:3]=='DFF':
            pin = cell.get_group('pin', 'Q')
        else:
            pin = cell.get_group('pin', 'Y')
        time_table= select_timing_table(pin,pin_name,'rise_transition')
        index=time_table.get_array('values')
        index2=time_table.get_array('index_2')
        if out_cap==index2[0][0]:
            delay= index[2][0]
        elif out_cap==index2[0][1]:
            delay= index[2][1]
        elif out_cap==index2[0][2]:
            delay= index[2][2]
        elif out_cap==index2[0][3]:
            delay= index[2][3]
        elif out_cap==index2[0][4]:
            delay= index[2][4]
        elif out_cap > index2[0][0] and out_cap < index2[0][1]:
            delay = self._interpolate(index2[0][0],index2[0][1],index[2][0], index[2][1],out_cap)
        elif out_cap > index2[0][1] and out_cap < index2[0][2]:
            delay = self._interpolate(index2[0][1],index2[0][2],index[2][1], index[2][2],out_cap)
        elif out_cap > index2[0][2] and out_cap < index2[0][3]:
            delay = self._interpolate(index2[0][2],index2[0][3],index[2][2], index[2][3],out_cap)
        elif out_cap > index2[0][3] and out_cap < index2[0][4]:
            delay = self._interpolate(index2[0][3],index2[0][4],index[2][3], index[2][4],out_cap)
        elif out_cap < index2[0][3]:
            delay = self._interpolate(index2[0][3],index2[0][4],index[2][0],index[2][1],out_cap)
        elif out_cap > index2[0][4]:
            delay = self._interpolate(index2[0][3],index2[0][4],index[2][3],index[2][4],out_cap)
        return delay
