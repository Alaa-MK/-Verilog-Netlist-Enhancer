module simple (
inp1,
inp2,
out
);

// Start PIs
input inp1;
input inp2;

// Start POs
output out;

// Start wires
wire n1;
wire n2;
wire n3;
wire n4;
wire inp1;
wire inp2;
wire out;

// Start cells
NAND2X1 u1 ( .A(inp1), .B(inp2), .Y(n1) );
NOR2X1 u5 (.A(n1), .B(inp1), .Y(n2));
XOR2X1 u6 (.A(n2), .B(n1), .Y(n3));
INVX1 u2 ( .A(n3), .Y(n4) );
INVX1 u3 ( .A(n4), .Y(out) );

endmodule
