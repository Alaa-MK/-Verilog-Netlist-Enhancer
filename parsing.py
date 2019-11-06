import re
import networkx as nx
import matplotlib.pyplot as plt
import sys
#sys.path.insert(1, '\pyverilog-1.1.4\examples')
#import example_parser


def get_ast(file_name):
    #exec(' .\pyverilog-1.1.4\examples\example_parser.py test.v > test.ast')  
    with open('{0}.ast'.format(file_name), 'r') as file:
        data = file.read()
    return data

def get_wires(ast):
    #parsing
    wires = re.findall('Wire: (.*?),', ast)
    wires_dict = {}
    for i in range (len(wires)):
        wires_dict[wires[i]]={}
        wires_dict[wires[i]]['destination']=[]
        wires_dict[wires[i]]['source']=''    
    instances = re.findall('Instance: (.*?)(InstanceList|\Z)', ast, re.DOTALL)
    
    #filling wires_dict
    for i in instances:
        cell_type=re.search(', (.*?) ', i[0])[0][2:-1]
        cell_name=re.search('\A(.*?),', i[0])[0][:-1]
        wires = re.findall('Identifier: (.*?) ', i[0])
        for w in wires[:-1]:
            wires_dict[w]['destination'].append(cell_name)
        wires_dict[wires[-1]]['source']=cell_name
    Icount = 1
    Ocount = 1
    I = 'i1'
    O ='o1'
    
<<<<<<< HEAD
    #Filling slots for the input and the output
    for w in wires_dict:
        if len(wires_dict[w]['destination']) == 0:
            wires_dict[w]['destination'].append(O)
            Ocount+=1
            O = 'o' + str(Ocount)
        if wires_dict[w]['source']=='':
            wires_dict[w]['source']= I
            Icount+=1
            I = 'i' + str(Icount)
    return wires_dict

def create_network(wires_dict):
    #Creating the Circuit DiGraph
    circuit = nx.DiGraph()
    
    #Creating the edge list of the circuit
    for w in wires_dict:
        for d in wires_dict[w]['destination']:
            s = wires_dict[w]['source']
            circuit.add_edge(s, d, label=wires_dict[w])
            
    return circuit
        

def main():
    ast = ''
    with open('test.ast', 'r') as file:
        ast = file.read()
        
    wires_dict = get_wires(ast)
    circuit = create_network(wires_dict)   
    nx.draw(circuit,with_labels = True)
    plt.show()    


if __name__=="__main__":
    main()
=======

instances = re.findall('Instance: (.*?)(InstanceList|\Z)', data, re.DOTALL)


#dictionary of cells: destination, source
for i in instances:
    cell_type=re.search(', (.*?) ', i[0])[0][2:-1]
    cell_name=re.search('\A(.*?),', i[0])[0][:-1]
    wires = re.findall('Identifier: (.*?) ', i[0])
    for w in wires[:-1]:
        wires_dict[w]['destination'].append(cell_name)
    wires_dict[wires[-1]]['source']=cell_name

Icount = 1
Ocount = 1
I = 'i1'
O ='o1'

#Filling slots for the input and the output
for w in wires_dict:
    if len(wires_dict[w]['destination']) == 0:
        wires_dict[w]['destination'].append(I)
        Icount+=1
        I = 'i' + str(Icount)
    if wires_dict[w]['source']=='':
        wires_dict[w]['source']= O
        Ocount+=1
        O = 'o' + str(Ocount)

#Creating the Circuit DiGraph
circuit = nx.DiGraph()


#Creatign the edge list of the circuit

for w in wires_dict:
    for d in wires_dict[w]['destination']:
        s = wires_dict[w]['source']
        circuit.add_node(s)
        circuit.add_node(d)
        circuit.add_edges((s, d), label=wires_dict[w])
        print (circuit.nodes())


print (circuit.edges())
nx.draw(circuit,with_labels = True)  
plt.show()

>>>>>>> 2fbb2ceaa47c0a5e42538515a2be2982369aa83c



