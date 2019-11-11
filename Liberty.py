from liberty.parser import parse_liberty
from liberty.types import select_timing_table
import re

class Liberty:
    def __init__(self, filename):
        self.library = parse_liberty(open(filename).read())
    
    def _interpolate(self, x1,x2,y1,y2,c): #interpolation function
        return y1 + (y2-y1)*(c-x1)/(x2-x1)

    def get_middle_capacitance(self): #a function to return the value of the middle capacitance 
        cell = self.library.get_group('cell', 'AND2X1')
        pin = cell.get_group('pin', 'Y')
        time_table= select_timing_table(pin,'A','rise_transition')
        index2=time_table.get_array('index_2')
        return index2[0][2]
    
    def get_pin_capacitance(self, cell_name, pin_name): #a function to return the capacitance of a certain input pin 
        cell = self.library.get_group('cell', cell_name) #for a certain cell
        assert cell is not None
        pin = cell.get_group('pin', pin_name)  
        capacitance = float(re.search('capacitance:(.*?);',str(pin))[0][13:-1])
        return capacitance
    
    def get_pin_delay(self, cell_name, pin_name, out_cap): #a function to return the delay of a certain arc 
                                                           #for a certain cell given the load capacitance

        cell = self.library.get_group('cell', cell_name)
        assert cell is not None
        if cell_name[0:3]=='DFF':
            pin = cell.get_group('pin', 'Q')
        else:
            pin = cell.get_group('pin', 'Y')

        time_table_rise= select_timing_table(pin,pin_name,'rise_transition')
        time_table_fall= select_timing_table(pin,pin_name,'fall_transition')

        index_rise=time_table_rise.get_array('values')
        index_fall=time_table_fall.get_array('values')

        #a new array to have the maximum value of the rising and falling delay
        index=time_table_rise.get_array('values')
        index[2][0]=max(index_rise[2][0],index_fall[2][0])   
        index[2][1]=max(index_rise[2][1],index_fall[2][1])
        index[2][2]=max(index_rise[2][2],index_fall[2][2])
        index[2][3]=max(index_rise[2][3],index_fall[2][3])
        index[2][4]=max(index_rise[2][4],index_fall[2][4])

        #delay calculation using interpolation
        index2=time_table_rise.get_array('index_2')
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
