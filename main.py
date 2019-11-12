from Netlist import Netlist
#from Liberty import Liberty
import matplotlib.pyplot as plt
import networkx as nx
import sys, getopt



def main(argv):
#    netlist = Netlist('test-cases/buffering_test.v')
#    #print(netlist.report_no_of_cells_of_each_type())
#    #print(netlist.max_fanout())
#    print(netlist.buffer_all(2))
#    print(netlist.cell_fanout('__buffer1__'))
#    #print('outputs:', netlist.outputs)
#    #print(netlist.netlist)
#    
#    g = netlist.get_graph()
#    #print(netlist.get_all_delays())
#    nx.draw(g,with_labels = True)
#    
#    plt.show()    
#    #print(netlist.cell_fanout('__buffer0__'))
#   # print(netlist.report_critical_path())
#    #print(netlist.report_max_delay())
#    
#    netlist.sizing_up(1.5)
#    #print(netlist.report_max_delay())
#    
    

    netlist= Netlist('test-cases/test.v', 'osu035.lib')
    g=netlist.get_graph()
    for e in g.edges():
        print(g.get_edge_data(e[0], e[1]))
    
#    
#    vfile=libfile=''
#    try:
#        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
#    except getopt.GetoptError:
#        print ('test.py -i <inputfile> -o <outputfile>')
#        sys.exit(2)
#    for opt, arg in opts:
#        if opt == '-h':
#            print ('test.py -v <verilog-file> -l <liberty-file>')
#            sys.exit()
#        elif opt in ("-v", "--vfile"):
#            vfile = arg
#        elif opt in ("-l", "--libfile"):
#            libfile = arg
#            
#    netlist = Netlist(vfile, libfile);
#    choice = ''
#    while choice.lower()!= 'quit':
#        choice = input('''Please choose an option of the following: 
#            delay: report the maximum delay of the circuit
#            n-cells: report the total number of cells in the circuit
#            fanout: report the max fanout of the circuit
#            buffer: satisfy the max fanout constraint using buffering
#            clone: try to satisfy the max fanout constraint using cloning
#            size: do greedy sizing algorithm to decrease the delay of the critical path
#            graph: visualize the circuit as a graph
#            netlist: print the current verilog netlist
#            quit: quit the program
#            
#            ''')
#        c = choice.lower()
#        if c=='delay':
#            print(netlist.report_max_delay())
#        elif c=='n-cells':
#            print(netlist.report_no_of_cells_of_each_type())
#        elif c=='fanout':
#            print(netlist.max_fanout())
#        elif c=='buffer':
#            netlist.buffer_all()
#            print('Max Fanout: ', netlist.max_fanout())
#        elif c=='clone':
#            netlist.clone_all()
#            print('Max Fanout: ', netlist.max_fanout())
#        elif c=='size':
#            print('Delay Before Sizing: ', netlist.max_delay())
#            netlist.sizing_up()
#            print('Delay After Sizing: ', netlist.max_delay())
#        elif c=='graph':
#            nx.draw(netlist.get_graph(),with_labels = True)
#            plt.show() 
#        elif c=='netlist':
#            print(netlist.to_v_netlist())
#        else:
#            print('Please choose a valid option.')
    
    
    
if __name__ == "__main__":
    main(sys.argv[1:])
    
