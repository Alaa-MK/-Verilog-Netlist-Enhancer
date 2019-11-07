import math
import re

class Netlist:
    def __init__(self, v_file_name):
        self.cell_names=['AND2X1','AND2X2','AOI21X1','AOI22X1','BUFX2','BUFX4','DFFNEGX1','NOR3X1',
            'DFFPOSX1','FAX1','HAX1','INVX1','INVX2','INVX4','INVX8','NAND2X1','NAND3X1','NOR2X1',
            'OAI21X1','OAI22X1','OR2X1','OR2X2','TBUFX1','TBUFX2','XOR2X1','MUX2X1','XNOR2X1',
            'LATCH','DFFSR','CLKBUF1','CLKBUF2','CLKBUF3']
        file = self._get_v_file_split(v_file_name)
        netlist_split = self._get_netlist_split(file)
        self.netlist = self._get_netlist_dict(netlist_split)
        self.buffer_count = 0
        self.buffer_wire_count = 0
        
    def _get_v_file_split(self, file_name):  
        with open(file_name, 'r') as file:
            data = file.readlines()
            data_split = [line.split(' ') for line in data]
        return data_split
    
    def _get_netlist_split(self, file_split):
        netlist = []
        for l in file_split:
            if l[0] in self.cell_names:
                netlist.append(l)
        return netlist
    
    def _get_netlist_dict(self, netlist_split):
        netlist = {}
        for l in netlist_split:
            netlist[l[1]]={'type':l[0]}
            for i in range (3, len(l)-1):
                arg = re.search('\..*\(', l[i])[0][1:-1]
                name = re.search('\(.*\)', l[i])[0][1:-1]
                netlist[l[1]][arg]=name
        return netlist
    
    def to_v_netlist(self):
        str = ''
        for key, value in self.netlist.items():
            line = '{0} {1} ( '.format(value['type'], key)
            for i in range (1,len(value)):
                line = line + '.{0}({1}), '.format(list(value.keys())[i], list(value.values())[i])
            line = line[:-2]+' );'+'\n'
            str = str + line
        return str
        
    def cell_inputs(self, cell_name):
        return list(self.netlist[cell_name].values())[1:-1]
        
    def cell_output(self, cell_name):
        return list(self.netlist[cell_name].values())[-1]
        
    def cell_fanout(self, cell_name):
        output_wire = self.cell_output(cell_name)
        counter = 0
        for key, value in self.netlist.items():
            counter += self.cell_inputs(key).count(output_wire)
        return counter
    
    def max_fanout(self):
        return max([self.cell_fanout(c) for c in list(self.netlist.keys())])
    
    #returns true if the netlist was modified
    def _buffer_one_level(self, cell_name, max_fanout):
        fanout = self.cell_fanout(cell_name)
        if fanout <= max_fanout:
            return False        #no violation
        b_in = self.cell_output(cell_name)
        n_buffers = min(max_fanout, math.ceil(fanout/max_fanout))
        b_wires = []
        
        #add buffers and connect to source
        for i in range (n_buffers):
            b_name = '__buffer__{0}'.format(self.buffer_count)
            self.buffer_count+=1
            b_wire_name = '__buffer_wire__{0}'.format(self.buffer_wire_count)
            self.buffer_wire_count+=1
            b_wires.append(b_wire_name)
            b_cell = {'type':'BUFX2', 'A':b_in, 'Y':b_wire_name}
            self.netlist[b_name]=b_cell
                    
        #connect buffers to destinations
        index = 0
        for key, value in self.netlist.items():
            for k2, v2 in list(value.items())[1:-1]:
                if b_in == v2 and key[:10] != '__buffer__':
                    self.netlist[key][k2]= b_wires[index%len(b_wires)]
                    index+=1
        return True
    
    def buffer_all(self, max_fanout):
        flag = True
        while flag:
            keys = list(self.netlist.keys())
            flag = any([self._buffer_one_level(key, max_fanout) for key in keys])