from Netlist import Netlist
from Liberty import Liberty

def main():
    netlist = Netlist('buffering_test.v')
    #netlist.buffer_all(2)
    netlist.clone_cell('u1', 3)
    print(netlist.to_v_netlist())
    #liberty = Liberty()
    
    
if __name__ == "__main__":
    main()