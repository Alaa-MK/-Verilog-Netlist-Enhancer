from Netlist import Netlist    

def main():
    netlist = Netlist('buffering_test.v')
    netlist.buffer_all(2)
    print(netlist.to_v_netlist())
    
if __name__ == "__main__":
    main()