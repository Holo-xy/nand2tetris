(SimpleFunction.test)
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@0
D=A
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@LCL
D=M
@1
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
A=A-1
M=D+M
@SP
A=M-1
M=!M
@ARG
D=M
@0
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
A=A-1
M=D+M
@ARG
D=M
@1
A=D+A
D=M
@SP
AM=M+1
A=A-1
M=D
@SP
AM=M-1
D=M
A=A-1
M=M-D
@LCL
D=M
@R14
M=D
@5
A=D-A
D=M
@R15
M=D
@ARG
D=M
@0
D=A+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R14
D=M-1
AM=D
D=M
@THAT
M=D
@R14
D=M-1
AM=D
D=M
@THIS
M=D
@R14
D=M-1
AM=D
D=M
@ARG
M=D
@R14
D=M-1
AM=D
D=M
@LCL
M=D
@R15
A=M
0;JMP
