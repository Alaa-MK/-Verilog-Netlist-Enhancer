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
output n2;
output n3;
output n4;
output n5;
output n6;
output n7;
output n8;
output n9;

// Start wires
wire n1;
wire n2;
wire n3;
wire n4;
wire n5;
wire inp1;
wire inp2;

// Start cells
NAND2X1 u1 ( .A(inp1), .B(inp2), .Y(n1) );
INVX1 u2 ( .A(n1), .Y(n2) );
INVX1 u3 ( .A(n1), .Y(n3) );
INVX1 u4 ( .A(n1), .Y(n4) );
INVX1 u5 ( .A(n1), .Y(n5) );
INVX1 u6 ( .A(n1), .Y(n6) );
INVX1 u7 ( .A(n1), .Y(n7) );
INVX1 u8 ( .A(n1), .Y(n8) );
INVX1 u9 ( .A(n1), .Y(n9) );

endmodule
