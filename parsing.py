import re
import networkx as nx
import matplotlib.pyplot as plt

with open('test.ast', 'r') as file:
    data = file.read()
    

wires = re.findall('Wire: (.*?),', data)

wires_dict = {}

for i in range (len(wires)):
    wires_dict[wires[i]]={}
    wires_dict[wires[i]]['destination']=[]
    wires_dict[wires[i]]['source']=''
    

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




