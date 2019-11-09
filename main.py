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
    nx.draw(g,with_labels = True)
    plt.show()    
    
if __name__ == "__main__":
    main()