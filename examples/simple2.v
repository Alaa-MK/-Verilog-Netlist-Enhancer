module simple (
inp1,
inp2,
out,
out2,
out3
);

// Start PIs
input inp1;
input inp2;

// Start POs
output out;
output out2;
output out3;

// Start wires
wire n1;
wire n2;
wire n3;
wire n4;
wire inp1;
wire inp2;
wire out;
wire out2;
wire out3;

// Start cells
NAND2X1 u1 ( .A(inp1), .B(inp2), .Y(n1) );
NOR2X1 u5 ( .A(n1), .B(inp1), .Y(n2) );
INVX1 u7 ( .A(n2), .Y(out2) );
INVX1 u8 ( .A(n2), .Y(out3) );
XOR2X1 u6 ( .A(n2), .B(n1), .Y(n3) );
INVX1 u2 ( .A(n3), .Y(n4) );
INVX1 u3 ( .A(n4), .Y(out) );

endmodule
