import re

with open('test.ast', 'r') as file:
    data = file.read()
    

wires = re.findall('Wire: (.*?),', data)
#print(wires)

wires_dict = {}

for i in range (len(wires)):
    wires_dict[wires[i]]={}
    wires_dict[wires[i]]['destination']=[]
    wires_dict[wires[i]]['source']=''
    

instances = re.findall('Instance: (.*?)(InstanceList|\Z)', data, re.DOTALL)
#print(instances)

#dictionary of cells: target, source

for i in instances:
    cell_type=re.search(', (.*?) ', i[0])[0][2:-1]
    cell_name=re.search('\A(.*?),', i[0])[0][:-1]
    #cells_dict[cell_name]['type']
    wires = re.findall('Identifier: (.*?) ', i[0])
    for w in wires[:-1]:
        wires_dict[w]['destination'].append(cell_name)
    wires_dict[wires[-1]]['source']=cell_name
print(wires_dict)
    
    

