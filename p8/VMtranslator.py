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
        instructions = '@SP\n' + 'A=M-1\n' + 'M=!M\n'
    elif command == 'neg':
        instructions = 'D=0\n' + '@SP\n' + 'A=M-1\n' + 'M=D-M\n'
    elif command == 'and':
        instructions = '@SP\n' + 'AM=M-1\n' + 'D=M\n' + 'A=A-1\n' + 'M=D&M\n'
    elif command == 'or':
        instructions = '@SP\n' + 'AM=M-1\n' + 'D=M\n' + 'A=A-1\n' + 'M=D|M\n'
    else:
        if command == 'eq': jump = 'JEQ'
        elif command == 'gt': jump = 'JGT'
        elif command == 'lt': jump = 'JLT'
        instructions = '@SP\n' + 'AM=M-1\n' + 'D=M\n' + '@SP\n' + 'A=M-1\n' + 'D=M-D\n' + 'M = 0\n' + f'@True{counter}\n' \
        +f'D;{jump}\n' + f'@False{counter}\n' + '0;JMP\n' + f'(True{counter})\n' + '@SP\n' + 'A=M-1\n' + 'M = -1\n' + f'(False{counter})\n'
        counter += 1
    return instructions,counter


class CodeWriter:
    def __init__(self,output_file):
        self.file_name = ''
        self.assembly_file = open(output_file,'w')
        self.LOGICAL_COUNTER = 0
        self.RETURN_COUNTER = 0
    def write_arithmatic(self,command):
        if command == 'add' or command == 'sub':
            instructions = handle_arithmatic_commands(command)
        else:
            instructions,self.LOGICAL_COUNTER = handle_logical_commands(command,self.LOGICAL_COUNTER)
        self.assembly_file.write(instructions)

    def write_push_pop(self,command,segment,index,is_pointer=False):
        instructions = handle_access_commands(command,segment,index,is_pointer,self.file_name)
        self.assembly_file.write(instructions)

    def write_label(self,label):
        instructions = f'({label})\n'
        self.assembly_file.write(instructions)

    def write_goto(self,label):
        instructions = f'@{label}\n' + '0;JMP\n'
        self.assembly_file.write(instructions)

    def write_if(self,label):
        instructions = '@SP\n' + 'AM=M-1\n' + 'D=M\n' + f'@{label}\n' + 'D;JNE\n'
        self.assembly_file.write(instructions)

    def write_function(self, function_name, num_vars):
        instructions = f'({function_name})\n'
        self.assembly_file.write(instructions)
        for n in range(int(num_vars)):
            self.write_push_pop('push', 'constant', 0)

    def write_call(self, function_name, num_args):
        ret_address = 'Return' + str(self.RETURN_COUNTER)
        instructions = f'@{ret_address}\n' + 'D=A\n' + '@SP\n' + 'AM=M+1\n' + 'A=A-1\n' + 'M=D\n'
        self.assembly_file.write(instructions)
        self.write_push_pop('push','LCL','0',True)
        self.write_push_pop('push', 'ARG', '0', True)
        self.write_push_pop('push', 'THIS', '0', True)
        self.write_push_pop('push', 'THAT', '0', True)
        instructions = '@SP\n' + 'D=M\n' + '@LCL\n' + 'M=D\n' + '@5\n' + 'D=D-A\n' + f'@{num_args}\n' 'D=D-A\n' + '@ARG\n' + 'M=D\n'
        instructions += f'@{function_name}\n' + '0;JMP\n' + f'({ret_address})\n'
        self.assembly_file.write(instructions)
        self.RETURN_COUNTER += 1

    def write_return(self):
        end_frame = '@LCL\n' + 'D=M\n' + '@R14\n' + 'M=D\n'
        ret_address = '@5\n' + 'A=D-A\n' + 'D=M\n' + '@R15\n' + 'M=D\n'
        self.assembly_file.write(end_frame + ret_address)

        self.write_push_pop('pop', 'ARG', '0')
        ARG_plus_one = '@ARG\n' + 'D=M\n' + '@SP\n' + 'M=D+1\n'
        self.assembly_file.write(ARG_plus_one)

        reset_THAT = '@R14\n' + 'D=M-1\n' + 'AM=D\n' + 'D=M\n' + '@THAT\n' + 'M=D\n'
        reset_THIS = '@R14\n' + 'D=M-1\n' + 'AM=D\n' + 'D=M\n' + '@THIS\n' + 'M=D\n'
        reset_ARG = '@R14\n' + 'D=M-1\n' + 'AM=D\n' + 'D=M\n' + '@ARG\n' + 'M=D\n'
        reset_LCL = '@R14\n' + 'D=M-1\n' + 'AM=D\n' + 'D=M\n' + '@LCL\n' + 'M=D\n'
        self.assembly_file.write(reset_THAT+reset_THIS+reset_ARG+reset_LCL)

        self.assembly_file.write('@R15\n' + 'A=M\n' + '0;JMP\n')

    def write_init(self):
        instructions = '@256\n' + 'D=A\n' + '@SP\n' + 'M=D\n'
        self.assembly_file.write(instructions)
        self.write_call('Sys.init',0)

    def set_file_name(self,file):
        self.file_name = file

    def Close(self):
        self.assembly_file.close()


class Parser:
    ARITHMATIC_COMMANDS = ['add', 'sub', 'eq', 'lt',  'gt', 'neg', 'not', 'and', 'or']
    def __init__(self, file):
        self.VM_file = open(file+'.vm', 'r')
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



def handle_path(path):
    if os.path.isdir(path):
        return [i for i in os.listdir(path) if i.endswith('.vm')]
    elif path.endswith('.vm'):
        return [os.path.basename(path)]
    else:
        raise ValueError('invalid path. path must be a directory or a .vm file.')

if __name__ == "__main__":
    import sys
    import os

    path = sys.argv[1]
    VM_files = handle_path(path)
    file_name = os.path.basename(path)
    if path.endswith('.vm'):
        path = os.path.dirname(path)
        file_name,_ = file_name.split('.',1)

    output_file = os.path.join(path, file_name + '.asm')
    codeWriter = CodeWriter(output_file)
    codeWriter.write_init() if 'Sys.vm' in VM_files else ''
    for file in VM_files:
        file, _ = file.split('.', 1)

        codeWriter.set_file_name(file)

        file = os.path.join(path,file)
        parser = Parser(file)

        while parser.has_more_commands():
            parser.advance()
            if not parser.command_type():
                continue
            if parser.command_type() == 'ARITHMATIC':
                codeWriter.write_arithmatic(parser.get_argument1())

            elif parser.command_type() == 'push' or parser.command_type() == 'pop':
                codeWriter.write_push_pop(parser.type, parser.get_argument1(), parser.get_argument2())

            elif parser.command_type() == 'label':
                codeWriter.write_label(parser.get_argument1())

            elif parser.command_type() == 'if-goto':
                codeWriter.write_if(parser.get_argument1())

            elif parser.command_type() == 'goto':
                codeWriter.write_goto(parser.get_argument1())

            elif parser.command_type() == 'call':
                codeWriter.write_call(parser.get_argument1(),parser.get_argument2())

            elif parser.command_type() == 'function':
                codeWriter.write_function(parser.get_argument1(),parser.get_argument2())

            elif parser.command_type() == 'return':
                codeWriter.write_return()
            else:
                raise Exception('enter a legal command.')
    codeWriter.Close()

