# -Verilog-Netlist-Enhancer
A utility to modify a given Verilog netlist to:
• Size up cells that have large fan-out
• Clone high fan-out cells
• Add buffers to high fan-out cells and distribute the loads between them
The utility accepts the Verilog netlist (to be enhanced) as well as the library liberty file. The user specifies the maximum
delay as well as the maximum fan-out for any cell in the design. The utility searches the netlist for the cells that violate
these 2 rules and applies the above techniques to resolve the violations.
