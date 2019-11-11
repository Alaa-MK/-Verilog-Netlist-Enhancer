# Verilog Netlist Enhancer
Implementation of a Verilog netlist modifier to enhance:
1. Maximum Fanout
2. Maximum Delay
By:
1. Sizing up cells with large fan-out 
2. Cloning high fan-out cells
3. Adding buffers to high fan-out cells
Given:
1. The Verilog netlist (to be enhanced) 
2. The library liberty file

# Getting Started
First, run the enhancer main file by typing the command
```
python main.py
```
Then, the program would ask to give the name of the verilog file as well as the library liberty file
 After successfully entering the file names the interface will display the following:
 
> Please choose an option of the following:
             delay: report the maximum delay of the circuit
             n-cells: report the total number of cells in the circuit
             fanout: report the max fanout of the circuit
             buffer: satisfy the max fanout constraint using buffering
             clone: try to satisfy the max fanout constraint using cloning
             size: do greedy sizing algorithm to decrease the delay of the critical path
             graph: visualize the circuit as a graph
             netlist: print the current verilog netlist
             quit: quit the program

And by entering any command, the program should apply the requested changes, and return the expected output

# Limitations

This enhancer does not supply:
1. optimization algorithms to enhance the delay and fanout
2. Enhanced visualization of the circuit


