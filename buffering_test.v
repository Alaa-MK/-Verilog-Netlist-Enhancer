module simple (
inp1,
inp2,
iccad_clk,
out
);

// Start PIs
input inp1;
input inp2;
input iccad_clk;

// Start POs
output out;

// Start wires
wire n1;
wire n2;
wire n3;
wire n4;
wire n5;
wire inp1;
wire inp2;

// Start cells
NAND2X1 u1 ( .A1(inp1), .A2(inp2), .ZN(n1) );
INVX1 u2 ( .A(n1), .ZN(n2) );
INVX1 u3 ( .A(n1), .ZN(n3) );
INVX1 u4 ( .A(n1), .ZN(n4) );
INVX1 u5 ( .A(n1), .ZN(n5) );
INVX1 u6 ( .A(n1), .ZN(n6) );
INVX1 u7 ( .A(n1), .ZN(n7) );
INVX1 u8 ( .A(n1), .ZN(n8) );
INVX1 u9 ( .A(n1), .ZN(n9) );

endmodule
