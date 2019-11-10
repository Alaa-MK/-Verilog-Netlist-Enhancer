import math
import re
import networkx as nx
from Liberty import Liberty

class Netlist:
    def __init__(self, v_file_name):
        self.liberty=Liberty()
        self.cell_names=['AND2X1','AND2X2','AOI21X1','AOI22X1','BUFX2','BUFX4','DFFNEGX1','NOR3X1',
            'DFFPOSX1','FAX1','HAX1','INVX1','INVX2','INVX4','INVX8','NAND2X1','NAND3X1','NOR2X1',
            'OAI21X1','OAI22X1','OR2X1','OR2X2','TBUFX1','TBUFX2','XOR2X1','MUX2X1','XNOR2X1',
            'LATCH','DFFSR','CLKBUF1','CLKBUF2','CLKBUF3']
        file = self._get_v_file_split(v_file_name)
        netlist_split = self._get_netlist_split(file)
        self.outputs = self._get_output_list(file)
        self.netlist = self._get_netlist_dict(netlist_split)
        self._update_load_capacitance()
        self._create_graph()
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

    def _get_output_list(self,file_split): #a function to get the outputs of the circuits in a list
        outputs = []
        for l in file_split:
            if l[0]=='output':
                outputs.append(l[1][0:-2])
        return outputs
    
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
        
    def cell_inputs(self, cell_name): #a function to return the list inputs of a certain cell instance
        return list(self.netlist[cell_name].values())[1:-2]
        
    def cell_output(self, cell_name): #a function to return the list outputs of a certain cell instance
        return list(self.netlist[cell_name].values())[-1]
        
    def cell_fanout(self, cell_name): #a function to return the fanout of a given cell instance
        output_wire = self.cell_output(cell_name)
        counter = 0
        for key, value in self.netlist.items():
            counter += self.cell_inputs(key).count(output_wire)
        return counter
    
    def max_fanout(self): #a function to return the maximum fanout in the circuit
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
        self._create_graph()
            
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
        self._create_graph()
                        
            
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
        for key, value in wires_dict.items():
            if key in self.outputs:
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
                    s = value['source']
                    if self.netlist[d]['type'][0:3]=='DFF':
                        self.g[s][d]['weight']= 0
                    else:
                        d_cell_type = self.netlist[d]['type']
                        d_cell_cap = self.netlist[d]['load_capacitance']
                        d_pin_name=''
                        for k2, v2 in list(self.netlist[d].items())[1:-2]:
                            if v2==key:
                                d_pin_name = k2
                        self.g[s][d]['weight']= self.liberty.get_pin_delay(d_cell_type, d_pin_name, d_cell_cap)
    
    def _split_on_FFs(self):
        countq=0
        edges_to_add = []
        edges_to_remove = []
        weights=[]
        for n in self.g.nodes:
            if n[0:2]!= '__':
                if self.netlist[n]['type'][0:3]=='DFF':
                    for i in self.g.out_edges(n):
                        edges_to_add.append(('q'+str(countq),i[1]))
                        edges_to_remove.append(i)
                        weights.append(self.g[i[0]][i[1]]['weight'])
                    countq+=1
        for i in range(len(edges_to_add)):
            self.g.add_edge(edges_to_add[i][0], edges_to_add[i][1])
            self.g[edges_to_add[i][0]][edges_to_add[i][1]]['weight']=weights[i]
        for e in edges_to_remove:
            self.g.remove_edge(e[0], e[1]) 

    def report_no_of_cells_of_each_type(self):
        cells_dict={}
        for c in self.cell_names:
            cells_dict[c]=0
        for key,value in self.netlist.items():
            cells_dict[value['type']]+=1
        return cells_dict

    def report_max_delay(self):
        return nx.dag_longest_path_length(self.g)
    
    def report_critical_path(self):
        return nx.dag_longest_path(self.g)
    
    def sizing_up(self):
        critical_p = self.report_critical_path()
        for n in critical_p:
            if (n[0]!= 'q') & (n[0:2]!= '__'):
                c_type =self.netlist[n]['type']
                c_type_new =c_type[0:-1]+str(int(c_type[len(c_type)-1])+1)
                if c_type_new in self.cell_names:
                    self.netlist[n]['type']=c_type_new
        self._update_load_capacitance() 
        self._create_graph()
                
                
    def _create_graph(self):
        self.g = nx.DiGraph()
        self._create_network()
        self._add_delay_to_graph()
        self._split_on_FFs()
        return self.g
    
    def get_graph(self):
        return self.g

    
    def get_all_delays(self):
        #self.create_graph()
        return self.g.edges.data()
    
    def max_delay(self):
        return nx.dag_longest_path_length(self.g);
    
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
        if self.cell_output(cell_name) in self.outputs:
            c+= self.liberty.get_middle_capacitance()
        return c
    
    def _update_load_capacitance(self):
        for key in self.netlist.keys():
            self.netlist[key]['load_capacitance']=self._get_output_capacitance(key)

    