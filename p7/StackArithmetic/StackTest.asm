@17
D=A
@SP
AM=M+1
A=A-1
M=D
@17
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True1
D;JEQ
@False1
0;JMP
(True1)
@SP
A=M-1
M = -1
(False1)
@17
D=A
@SP
AM=M+1
A=A-1
M=D
@16
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True2
D;JEQ
@False2
0;JMP
(True2)
@SP
A=M-1
M = -1
(False2)
@16
D=A
@SP
AM=M+1
A=A-1
M=D
@17
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True3
D;JEQ
@False3
0;JMP
(True3)
@SP
A=M-1
M = -1
(False3)
@892
D=A
@SP
AM=M+1
A=A-1
M=D
@891
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True4
D;JLT
@False4
0;JMP
(True4)
@SP
A=M-1
M = -1
(False4)
@891
D=A
@SP
AM=M+1
A=A-1
M=D
@892
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True5
D;JLT
@False5
0;JMP
(True5)
@SP
A=M-1
M = -1
(False5)
@891
D=A
@SP
AM=M+1
A=A-1
M=D
@891
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True6
D;JLT
@False6
0;JMP
(True6)
@SP
A=M-1
M = -1
(False6)
@32767
D=A
@SP
AM=M+1
A=A-1
M=D
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True7
D;JGT
@False7
0;JMP
(True7)
@SP
A=M-1
M = -1
(False7)
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
@32767
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True8
D;JGT
@False8
0;JMP
(True8)
@SP
A=M-1
M = -1
(False8)
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
@32766
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D = M
@SP
A=M-1
D=M-D
M = 0
@True9
D;JGT
@False9
0;JMP
(True9)
@SP
A=M-1
M = -1
(False9)
@57
D=A
@SP
AM=M+1
A=A-1
M=D
@31
D=A
@SP
AM=M+1
A=A-1
M=D
@53
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
A=A-1
M=D+M
@112
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
A=A-1
M=M-D
D=0
@SP
A=M-1
M=D-M
@SP
AM=M-1
D=M
A=A-1
M=D&M
@82
D=A
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
A=A-1
M=D|M
@SP
A=M-1
M=!M
