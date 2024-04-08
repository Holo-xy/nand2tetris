symbolTable = {
    'SCREEN': '16384'
    , 'KBD': '24567'
    , 'SP': '0'
    , 'LCL': '1'
    , 'ARG': '2'
    , 'THIS': '3'
    , 'THAT': '4'
    , "R0": '0'
    , "R1": '1'
    , "R2": '2'
    , "R3": '3'
    , "R4": '4'
    , "R5": '5'
    , "R6": '6'
    , "R7": '7'
    , "R8": '8'
    , "R9": '9'
    , "R10": '10'
    , "R11": '11'
    , "R12": '12'
    , "R13": '13'
    , "R14": '14'
    , "R15": '15'
}


def firstPass(assembly_file='assembly.asm'):
    f = open(assembly_file, 'r')
    programCounter = -1
    for l in f:
        programCounter += 1
        l = l.strip()
        if l.startswith('//') or not l:
            programCounter -= 1
        elif l.startswith('('):
            symbolTable[l[1:-1]] = programCounter
            programCounter -= 1
    f.close()


def AHandler(num, flag=0):
    if flag:
        num = symbolTable[num]
    num = int(num)
    binary = bin(num)
    binary = ('0' * (16 - len(binary) + 2)) + binary[2:]
    return binary


def CHandler(s):
    A, D, M = 0, 0, 0
    L, E, G = 0, 0, 0
    a, c1, c2, c3, c4, c5, c6 = 0, 0, 0, 0, 0, 0, 0
    dest, comp, jump = '', '', ''
    if '=' in s:
        dest, comp = s.split('=', 1)
    if ';' in s and s[-1] != ';':
        comp, jump = s.split(';', 1)
        if '=' in comp:
            dest, comp = comp.split('=', 1)
    if jump:
        if 'L' in jump: L = 1
        if 'E' in jump: E = 1
        if 'G' in jump: G = 1
        if jump == 'JMP': G = E = L = 1
        if jump == 'JNE': L = G = 1;E = 0

    jump = str(L) + str(E) + str(G)
    if dest:
        # print('dest')
        if 'A' in dest: A = 1
        if 'M' in dest: M = 1
        if 'D' in dest: D = 1
    dest = str(A) + str(D) + str(M)

    if comp:
        if 'M' in comp:
            a = 1
            comp = comp.replace('M', 'A')
        if comp == '0':
            c1 = c3 = c5 = 1
        elif comp == '1':
            c1 = c2 = c3 = c4 = c5 = c6 = 1
        elif comp == '-1':
            c1 = c2 = c3 = c5 = 1
        elif comp == 'D':
            c3 = c4 = 1
        elif comp == 'A':
            c1 = c2 = 1
        elif comp == '!D':
            c3 = c4 = 1;
            c6 = 1
        elif comp == '!A':
            c1 = c2 = 1;
            c6 = 1
        elif comp == '-D':
            c2 = c3 = 1;
            c5 = c6 = 1
        elif comp == '-A':
            c1 = c2 = 1;
            c5 = c6 = 1
        elif comp == 'D+1':
            c2 = c3 = c4 = 1;
            c5 = c6 = 1
        elif comp == 'A+1':
            c1 = c2 = 1;
            c4 = c5 = c6 = 1
        elif comp == 'D-1':
            c3 = c4 = 1;
            c5 = 1
        elif comp == 'A-1':
            c1 = c2 = 1;
            c5 = 1
        elif comp == 'D+A' or comp == 'A+D':
            c5 = 1
        elif comp == 'D-A':
            c2 = c5 = c6 = 1
        elif comp == 'A-D':
            c4 = c5 = c6 = 1
        elif comp == 'D|A':
            c2 = c4 = c6 = 1
    comp = str(c1) + str(c2) + str(c3) + str(c4) + str(c5) + str(c6)
    binary = '111' + str(a) + comp + dest + jump
    return binary


def secondPass(assembly_file='assembly.asm', hack_file='binary.hack'):
    f = open(assembly_file, 'r')
    n = 16
    assembly = open(hack_file, 'w')
    w = ''
    for l in f:
        l = l.strip()
        l = l.replace(" ", "")
        index = l.find('//')
        if index != -1 and index != 0:
            l = l[:index]
        if not l or l.startswith('//') or l.startswith('('):
            continue
        elif l.startswith('@'):
            if ord(l[1]) in range(48, 58):
                w = AHandler(l[1:])
            elif symbolTable.get(l[1:]) is not None:
                w = AHandler(l[1:], 1)
            else:
                symbolTable[l[1:]] = str(n)
                w = AHandler(l[1:], 1)
                n += 1
        else:
            w = CHandler(l)
        w += '\n'
        assembly.write(w)
    f.close()


firstPass()
secondPass()
