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

## Dependencies
1. Python3: 3.8 
2. NetworkX 1.9
```
pip install networkx
```
3. Liberty-parser 0.0.4
```
pip install liberty-parser
```
4.Regex 2019.11.1
```
pip install regex
```
5. Matplotlib 3.1.1
```
pip install matplotlib
```

## Assumptions
1. Each cell has only one output
2. The list of the supported cells types is as follows:
['AND2X1','AND2X2','AOI21X1','AOI22X1','BUFX2','BUFX4','DFFNEGX1','NOR3X1',
'DFFPOSX1','FAX1','HAX1','INVX1','INVX2','INVX4','INVX8','NAND2X1','NAND3X1','NOR2X1',
'OAI21X1','OAI22X1','OR2X1','OR2X2','TBUFX1','TBUFX2','XOR2X1','MUX2X1','XNOR2X1',
'LATCH','DFFSR','CLKBUF1','CLKBUF2','CLKBUF3']

## Building and Running
First, run the enhancer main file by typing the command
```
python main.py
```
##Tools
After running the main file, the program would ask to give the name of the verilog file as well as the library liberty file
 After successfully entering the file names the interface will display the following:
 
**Please choose an option of the following:**

**delay:** report the maximum delay of the circuit

**n-cells:** report the total number of cells in the circuit

**fanout:** report the max fanout of the circuit

**buffer:** satisfy the max fanout constraint using buffering

**clone:** try to satisfy the max fanout constraint using cloning

**size:** do greedy sizing algorithm to decrease the delay of the critical path

**graph:** visualize the circuit as a graph

**netlist:** print the current verilog netlist

**quit:** quit the program

And by entering any command, the program should apply the requested changes, and return the expected output

## Limitations

This enhancer does not supply:
1. calculating the delay for the rising and falling transitions of the inputs, it always chooses the larger transiton delay
2. Optimization algorithms to enhance the delay and fanout
3. An enhanced visualization of the circuit


