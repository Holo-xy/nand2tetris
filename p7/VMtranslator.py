import sys
import os

def handle_push(segment, index, is_pointer):
    if segment == 'constant':
        instructions = '@' + str(index) + '\n' + 'D=A\n'
        instructions += '@SP\n' + 'AM=M+1\n' + 'A=A-1\n' + 'M=D\n'
        return instructions

    elif segment == 'temp':
        instructions = '@' + str(index + 5) + '\n' + 'D=M\n'
        instructions += '@SP\n' + 'AM=M+1\n' + 'A=A-1\n' + 'M=D\n'
        return instructions

    is_pointer_push = f'@{index}\n' + 'A=D+A\n' + 'D=M\n'
    if is_pointer:
        is_pointer_push = ''

    instructions = f'@{segment}\n' + 'D=M\n' + is_pointer_push + '@SP\n' + 'AM=M+1\n' + 'A=A-1\n' + 'M=D\n'
    return instructions


def handle_pop(segment, index, is_pointer):
    if segment == 'temp':
        instructions = '@' + str(index + 5) + '\n' + 'D=A\n'
        instructions += '@R13\n' + 'M=D\n' + '@SP\n' + 'AM=M-1\n' + 'D=M\n' + '@R13\n' + 'A=M\n' + 'M=D\n'
        return instructions

    is_pointer_pop = 'D=M\n' + f'@{index}\n' + 'D=A+D\n'
    if is_pointer:
        is_pointer_pop = 'D=A\n'

    instructions = f'@{segment}\n' + is_pointer_pop + '@R13\n' + 'M=D\n' + '@SP\n' + 'AM=M-1\n' + 'D=M\n' + '@R13\n' + 'A=M\n' + 'M=D\n'
    return instructions


def handle_access_commands(command, segment, index, is_pointer=False, file_name=''):
    index = int(index)
    if segment == 'pointer':
        segment = 'THAT' if index else 'THIS'
        is_pointer = True
    elif segment == 'local':
        segment = 'LCL'
    elif segment == 'argument':
        segment = 'ARG'
    elif segment == 'this':
        segment = 'THIS'
    elif segment == 'that':
        segment = 'THAT'
    elif segment == 'static':
        segment = f'{file_name}.{index}'
        is_pointer = True

    if command == 'push':
        return handle_push(segment, index, is_pointer)
    elif command == 'pop':
        return handle_pop(segment, index, is_pointer)


def handle_arithmatic_commands(command):
    if command.startswith('add'):
        return '@SP\n' + 'AM=M-1\n' + 'D=M\n' + 'A=A-1\n' + 'M=D+M\n'
    elif command.startswith('sub'):
        return '@SP\n' + 'AM=M-1\n' + 'D=M\n' + 'A=A-1\n' + 'M=M-D\n'


def handle_logical_commands(command,counter):
    jump = ''
    if command == 'not':
        w = '@SP\n' + 'A=M-1\n' + 'M=!M\n'
    elif command == 'neg':
        w = 'D=0\n' + '@SP\n' + 'A=M-1\n' + 'M=D-M\n'
    elif command == 'and':
        w = '@SP\n' + 'AM=M-1\n' + 'D=M\n' + 'A=A-1\n' + 'M=D&M\n'
    elif command == 'or':
        w = '@SP\n' + 'AM=M-1\n' + 'D=M\n' + 'A=A-1\n' + 'M=D|M\n'
    else:
        counter += 1
        if command == 'eq': jump = 'JEQ'
        elif command == 'gt': jump = 'JGT'
        elif command == 'lt': jump = 'JLT'
        w = '@SP\n' + 'AM=M-1\n' + 'D = M\n' + '@SP\n' + 'A=M-1\n' + 'D=M-D\n' + 'M = 0\n' + f'@True{counter}\n' \
        +f'D;{jump}\n' + f'@False{counter}\n' + '0;JMP\n' + f'(True{counter})\n' + '@SP\n' + 'A=M-1\n' + 'M = -1\n' + f'(False{counter})\n'

    return w,counter



class CodeWriter:
    def __init__(self,output_file):
        self.file = os.path.basename(output_file)
        self.assembly_file = open(output_file + '.asm','w')
        self.LOGICAL_COUNTER = 0

    def write_arithmatic(self,command):
        if command == 'add' or command == 'sub':
            instructions = handle_arithmatic_commands(command)
        else:
            instructions,self.LOGICAL_COUNTER = handle_logical_commands(command,self.LOGICAL_COUNTER)
        self.assembly_file.write(instructions)

    def write_push_pop(self,command,segment,index,is_pointer=False):
        instructions = handle_access_commands(command,segment,index,is_pointer,self.file)
        self.assembly_file.write(instructions)

    def Close(self):
        self.assembly_file.close()


class Parser:
    ARITHMATIC_COMMANDS = ['add', 'sub', 'eq', 'lt', 'gt', 'neg', 'not', 'and', 'or']

    def __init__(self, input_file):
        input_file += '.vm'
        self.VM_file = open(input_file, 'r')
        self.line = ''
        self.argument1 = ''
        self.argument2 = ''
        self.type = ''

    def has_more_commands(self):
        position = self.VM_file.tell()
        char = self.VM_file.read(1)
        self.VM_file.seek(position)
        return bool(char)

    def advance(self):
        self.type = ''
        self.line = self.VM_file.readline()
        self.parse()

    def command_type(self):
        return self.type

    def parse(self):
        if self.line.startswith('//'):
            return
        self.line = self.line.split('//')[0].strip()
        self.line = self.line.strip()
        words = self.line.split(' ')
        command = words[0]

        self.type = command
        self.argument1 = words[1] if len(words) > 1 else ''
        self.argument2 = words[2] if len(words) > 2 else ''

        if command in self.ARITHMATIC_COMMANDS:
            self.type = 'ARITHMATIC'
            self.argument1 = command

    def get_argument1(self):
        return self.argument1

    def get_argument2(self):
        return self.argument2


if __name__ == "__main__":
    path = sys.argv[1]
    file_name = os.path.basename(path)
    if path.endswith('.vm'):
        path = os.path.dirname(path)
        file_name,_ = file_name.split('.',1)
    file = os.path.join(path, file_name)

    parser = Parser(file)
    codeWriter = CodeWriter(file)

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == 'ARITHMATIC':
            codeWriter.write_arithmatic(parser.get_argument1())
        elif parser.command_type() == 'push' or parser.command_type() == 'pop':
            codeWriter.write_push_pop(parser.type,parser.get_argument1(),parser.get_argument2())
    codeWriter.Close()