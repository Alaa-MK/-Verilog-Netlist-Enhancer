from Netlist import Netlist
from Liberty import Liberty

def main():
    netlist = Netlist('buffering_test.v')
    netlist.buffer_all(2)
    #print(netlist.to_v_netlist())
    liberty = Liberty()
    print(liberty.get_capacitance('AND2X1', 'A'))
    
    
if __name__ == "__main__":
    main()