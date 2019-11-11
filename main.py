from Netlist import Netlist
#from Liberty import Liberty
import matplotlib.pyplot as plt
import networkx as nx



def main():
    netlist = Netlist('buffering_test.v')
    #print(netlist.report_no_of_cells_of_each_type())
    #print(netlist.max_fanout())
    print(netlist.buffer_all(2))
    print(netlist.cell_fanout('__buffer1__'))
    #print('outputs:', netlist.outputs)
    #print(netlist.netlist)
    
    g = netlist.get_graph()
    #print(netlist.get_all_delays())
    nx.draw(g,with_labels = True)
    
    plt.show()    
    #print(netlist.cell_fanout('__buffer0__'))
   # print(netlist.report_critical_path())
    #print(netlist.report_max_delay())
    
    netlist.sizing_up()
    #print(netlist.report_max_delay())
    
    
if __name__ == "__main__":
    main()
    
