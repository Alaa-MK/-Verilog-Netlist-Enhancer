from Netlist import Netlist
#from Liberty import Liberty
import matplotlib.pyplot as plt
import networkx as nx



def main():
    netlist = Netlist('test.v')
    #netlist.buffer_all(2)
    #netlist.clone_cell('u1', 3)
    #print(netlist.to_v_netlist())
    #liberty = Liberty()
    
    g = netlist.create_graph()
    print(netlist.get_all_delays())
    nx.draw(g,with_labels = True)
    plt.show()    
    
if __name__ == "__main__":
    main()
    
    '''
    
    
[('__i1__', 'u1', {'label': 'inp1', 'weight': 0.27184447380000004}), 
('u1', 'u4', {'label': 'n1', 'weight': 0.24911771460000004}), 
('__i2__', 'u1', {'label': 'inp2', 'weight': 0.24793342140000002}),
 ('u4', 'f1', {'label': 'n2', 'weight': 0}), 
 ('__i3__', 'f1', {'label': 'iccad_clk', 'weight': 0}),
 ('u2', 'u3', {'label': 'n4', 'weight': 0.24359999999999998}), 
 ('u3', '__o1__', {'label': 'out'}),
 ('q0', 'u2', {'weight': 0.24359999999999998}), 
 ('q0', 'u4', {'weight': 0.24911771460000004})]
'''