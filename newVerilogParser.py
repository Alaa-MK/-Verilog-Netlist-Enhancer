import re

cell_names=['AND2X1','AND2X2','AOI21X1','AOI22X1','BUFX2','BUFX4','DFFNEGX1','NOR3X1',
            'DFFPOSX1','FAX1','HAX1','INVX1','INVX2','INVX4','INVX8','NAND2X1','NAND3X1','NOR2X1',
            'OAI21X1','OAI22X1','OR2X1','OR2X2','TBUFX1','TBUFX2','XOR2X1','MUX2X1','XNOR2X1',
            'LATCH','DFFSR','CLKBUF1','CLKBUF2','CLKBUF3']

class Netlist:
    def __init__(self, v_file_name):
        file = self._get_v_file_split('test.v')
        netlist_split = self._get_netlist_split(file)
        self.netlist = self._get_netlist_dict(netlist_split)
        
    def _get_v_file_split(self, file_name):  
        with open(file_name, 'r') as file:
            data = file.readlines()
            data_split = [line.split(' ') for line in data]
        return data_split
    
    def _get_netlist_split(self, file_split):
        netlist = []
        for l in file_split:
            if l[0] in cell_names:
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
    
    def export_v(self):
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


def main():
    netlist = Netlist('test.v')
    print(netlist.max_fanout())
    
    
if __name__ == "__main__":
    main()