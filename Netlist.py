import math
import re
import networkx as nx
from Liberty import Liberty

class Netlist:
    def __init__(self, v_file_name):
        self.liberty=Liberty()
        self.g = nx.DiGraph()
        self.cell_names=['AND2X1','AND2X2','AOI21X1','AOI22X1','BUFX2','BUFX4','DFFNEGX1','NOR3X1',
            'DFFPOSX1','FAX1','HAX1','INVX1','INVX2','INVX4','INVX8','NAND2X1','NAND3X1','NOR2X1',
            'OAI21X1','OAI22X1','OR2X1','OR2X2','TBUFX1','TBUFX2','XOR2X1','MUX2X1','XNOR2X1',
            'LATCH','DFFSR','CLKBUF1','CLKBUF2','CLKBUF3']
        file = self._get_v_file_split(v_file_name)
        netlist_split = self._get_netlist_split(file)
        self.netlist = self._get_netlist_dict(netlist_split)
        self._update_load_capacitance()
        self.cell_count = 0
        self.wire_count = 0
        
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
        return list(self.netlist[cell_name].values())[1:-2]
        
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
            b_name = '__buffer{0}__'.format(self.cell_count)
            self.cell_count+=1
            b_wire_name = '__wire{0}__'.format(self.wire_count)
            self.wire_count+=1
            b_wires.append(b_wire_name)
            b_cell = {'type':'BUFX2', 'A':b_in, 'Y':b_wire_name}
            self.netlist[b_name]=b_cell
                    
        #connect buffers to destinations
        index = 0
        for key, value in self.netlist.items():
            for k2, v2 in list(value.items())[1:-2]:
                if b_in == v2 and key[:8] != '__buffer':
                    self.netlist[key][k2]= b_wires[math.floor(index/(fanout/n_buffers))]
                    index+=1
        return True
    
    def buffer_all(self, max_fanout):
        flag = True
        while flag:
            keys = list(self.netlist.keys())
            flag = any([self._buffer_one_level(key, max_fanout) for key in keys])
        self._update_load_capacitance()
            
    #clones the cell into two and divides outputs 
    def clone_cell(self, cell_name, n_clones):
        c_output=self.cell_output(cell_name)
        n = min(n_clones, self.cell_fanout(cell_name))  # you shouldn't create clones more than the fanout
        fanout=self.cell_fanout(cell_name)
        wires = []
        wires.append(c_output)
        #add clones and connect to source inputs
        for i in range (n-1):
            c_name = '__cell{0}__'.format(self.cell_count)
            self.cell_count+=1
            wire_name = '__wire{0}__'.format(self.wire_count)
            self.wire_count+=1
            wires.append(wire_name)
            cell = self.netlist[cell_name].copy()
            cell[list(cell.keys())[-1]] = wire_name
            self.netlist[c_name]=cell
                    
        #connect cells to destinations
        index = 0
        for key, value in self.netlist.items():
            for k2, v2 in list(value.items())[1:-2]:
                if c_output == v2:
                    self.netlist[key][k2]= wires[math.floor(index/(fanout/n))]
                    index+=1 
        self._update_load_capacitance()
                        
            
    def _get_wires_dict(self):
        wires_temp = [list(d.values())[1:-1] for d in self.netlist.values()]
        wires = []
        for w in wires_temp:
            wires+=w
        
        wires_dict = {}
        for i in range (len(wires)):
            wires_dict[wires[i]]={}
            wires_dict[wires[i]]['destination']=[]
            wires_dict[wires[i]]['source']=''    
        
        #filling wires_dict
        for key, value in self.netlist.items():
            for w in list(value.values())[1:-2]:
                wires_dict[w]['destination'].append(key)
            wires_dict[list(value.values())[-2]]['source']=key
            
        #return wires_dict
        
        Icount = 1
        Ocount = 1
        I = '__i1__'
        O ='__o1__'
        #Filling slots for the input and the output
        print (wires_dict)
        for key, value in wires_dict.items():
            if len(value['destination']) == 0:
                wires_dict[key]['destination'].append(O)
                Ocount+=1
                O = '__o{0}__'.format(Ocount)
            if value['source']=='':
                wires_dict[key]['source']= I
                Icount+=1
                I = '__i{0}__'.format(Icount)
                
        return wires_dict

    
    def _create_network(self):
        wires_dict = self._get_wires_dict()
        #Creating the edge list of the circuit
        for w in wires_dict:
            for d in wires_dict[w]['destination']:
                s = wires_dict[w]['source']
                self.g.add_edge(s, d, label=w)
    
    def _add_delay_to_graph(self):
        wires_dict = self._get_wires_dict()
        for key, value in wires_dict.items():
            for d in value['destination']:
                if d[0:2]!='__':
                    #print(self.netlist[d])
                    s = value['source']
                    d_cell_type = self.netlist[d]['type']
                    d_cell_cap = self.netlist[d]['load_capacitance']
                    d_pin_name=''
                    for k2, v2 in list(self.netlist[d].items())[1:-2]:
                        if v2==key:
                            d_pin_name = k2
                    self.g[s][d]['weight']= self.liberty.get_pin_delay(d_cell_type, d_pin_name, d_cell_cap)
    
    def _split_on_FFs(self):
        countq=0
        for e in self.g.edges:
            print(e[0][0:2]!= '__')
            if e[0][0:2]!= '__':
                if self.netlist[e[0]]['type'][0:3]=='DFF':
                    self.g.add_edge('q'+str(countq),e[1])
                    countq+=1
                    self.g.remove_edge(e)
                
    def create_graph(self):
        self._create_network()
        #self._split_on_FFs()
        #self._add_delay_to_graph()
        return self.g

    def split_on_FFs(self):
        countq=0
        for e in self.g.edges:
            if(e[0][0:2]!='__'):
                if(self.netlist[e[0]]['type'][0:3]=='DFF'):
                    self.g.add_edge('q'+str(countq),e[1])
                    countq+=1
                    self.g.remove_edge(e)

    
    def get_all_delays(self):
        self.create_graph()
        return self.g
    
    def _wire_destinations(self, wire_name):
        destinations=[]
        for key, value in self.netlist.items():
            for k2, v2 in list(value.items())[1:-2]:
                if v2==wire_name:
                    destinations.append([value['type'], k2])
        return destinations 
    
    def _get_output_capacitance(self, cell_name):
        destinations = self._wire_destinations(self.cell_output(cell_name))
        c = 0
        for d in destinations:
            c+= self.liberty.get_pin_capacitance(d[0],d[1])
        return c
    
    def _update_load_capacitance(self):
        for key in self.netlist.keys():
            self.netlist[key]['load_capacitance']=self._get_output_capacitance(key)

    