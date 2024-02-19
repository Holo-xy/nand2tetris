// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

//Check if R0,R1 <= 0
// 	   set @2 = 0, jump to end
@1
D = M
@counter
M = D
@0
D = M
@2 
M = 0
@END
D;JLE
@1
D = M
@2 
M = 0
@END
D;JLE

// add @0 @1 times
(LOOP)
@0
D = M
@2
M = M + D
@counter
M = M - 1
D = M
@END
D;JLE
@counter
M = D
@LOOP
0;JMP

(END)
@END
0;JMP