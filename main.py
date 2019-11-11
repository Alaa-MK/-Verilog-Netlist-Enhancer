from Netlist import Netlist
#from Liberty import Liberty
import matplotlib.pyplot as plt
import networkx as nx
import sys, getopt



def main(argv):

    vfile=input('please enter the name of the v file: ')
    libfile = input('please enter the name of the liberty file: ')
            
    netlist = Netlist(vfile, libfile)   
    choice = ''
    while True:
        choice = input('''Please choose an option of the following: 
            delay: report the maximum delay of the circuit
            n-cells: report the total number of cells in the circuit
            fanout: report the max fanout of the circuit
            buffer: satisfy the max fanout constraint using buffering
            clone: try to satisfy the max fanout constraint using cloning
            size: do greedy sizing algorithm to decrease the delay of the critical path
            graph: visualize the circuit as a graph
            netlist: print the current verilog netlist
            quit: quit the program
            
            ''')
        c = choice.lower()
        if c=='delay':
            print(netlist.report_max_delay())
        elif c=='n-cells':
            print(netlist.report_no_of_cells_of_each_type())
        elif c=='fanout':
            print(netlist.max_fanout())
        elif c=='buffer':
            fo = input("please enter the desired max fanout: ")
            netlist.buffer_all(int(fo))
            print('Max Fanout: ', netlist.max_fanout())
        elif c=='clone':
            fo = input("please enter the desired max fanout: ")
            netlist.clone_all(int(fo))
            print('Max Fanout: ', netlist.max_fanout())
        elif c=='size':
            delay = input("please enter the desired max delay: ")
            print('Delay Before Sizing: ', netlist.report_max_delay())
            netlist.sizing_up(float(delay))
            print('Delay After Sizing: ', netlist.report_max_delay())
        elif c=='graph':
            nx.draw(netlist.get_graph(),with_labels = True)
            plt.show() 
        elif c=='netlist':
            print(netlist.to_v_netlist())
        elif c=='quit':
            return
        else:
            print('Please choose a valid option.')
        
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
