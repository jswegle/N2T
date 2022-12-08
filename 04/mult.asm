// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@2
M=0
@0
D=M
(LOOP)
  @END
  D;JEQ
  @1
  D=M
  @2
  M=D+M
  @0
  M=M-1
  D=M
  @LOOP
  0;JMP
(END)
  0;JMP
