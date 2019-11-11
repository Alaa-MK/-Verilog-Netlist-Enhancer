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
wire inp1;
wire inp2;
wire iccad_clk;
wire out;

// Start cells
NAND2X1 u1 ( .A(inp1), .B(inp2), .Y(n1) );
DFFPOSX1 f1 ( .D(n2), .CLK(iccad_clk), .Q(n3) );
INVX1 u2 ( .A(n3), .Y(n4) );
INVX1 u3 ( .A(n4), .Y(out) );
NOR2X1 u4 ( .A(n1), .B(n3), .Y(n2) );

endmodule