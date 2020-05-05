import sys
import re


class execution_unit(object):

    def __init__(self, register_file, BIU):
        self.IR = []                 # 指令寄存器
        self.opcode = ''             # 操作码
        self.oprands = []            # 操作数
        self.eo = [0] * 5            # Evaluated operands
        self.GR = register_file.GR   # AX BX CX DX
        self.FR = register_file.FR   # Flag Register
        self.SP = register_file.SP
        self.BP = register_file.BP
        self.SI = register_file.SI
        self.DI = register_file.DI

        self.bus = BIU # 内部总线连接BIU

    def run(self):
        self.IR = self.bus.instruction_queue.get()
        self.opcode = self.IR[0]
        if len(self.IR) > 1:
            self.oprands = self.IR[1:]
        self.instruction_decoder()
        self.evaluate_all_oprands()
        self.control_circuit()

    def read_cache(self, location):
        return self.bus.read_cache(location)

    def evaluate_parameter(self, operand):
        # read register
        for reg in self.GR.list:
            if reg in operand:
                operand = operand.replace(reg, str(self.GR.read(reg)))
        # access memory
        if '[' in operand:
            operand = operand.replace('[', '').replace(']', '')
            operand = self.read_cache(operand)
        return int(operand)

    def evaluate_all_oprands(self):
        for i in range(len(self.oprands)):
            self.eo[i] = self.evaluate_parameter(self.oprands[i])

    def instruction_decoder(self):
        # 数制转换
        ins = self.oprands
        if len(ins) < 1:
            return
        for i in range(len(ins)):
            # 十六进制转换为十进制
            hex_number = re.findall(r'[0-9A-F]+H', ins[i])
            if hex_number:
                ins[i] = ins[i].replace(hex_number[0], str(int(hex_number[0].strip('H'), 16)))
            # 二进制转换为十进制
            bin_number = re.findall(r'[01]+B', ins[i])
            if bin_number:
                ins[i] = ins[i].replace(bin_number[0], str(int(bin_number[0].strip('B'), 2)))

    def control_circuit(self):
        data_transfer_ins = ['MOV', 'XCHG', 'LEA', 'LDS', 'LES']
        arithmetic_ins = ['ADD', 'SUB', 'INC', 'DEC', 'MUL', 'IMUL', 'DIV', 'IDIV']
        logical_ins = ['AND', 'OR', 'XOR', 'NOT', 'NEG', 'CPM', 'TEST']
        rotate_shift_ins = ['RCL', 'RCR'] 
        transfer_control_ins = ['JMP', 'RET', 'JA', 'LOOP', 'RET', 'CALL']
        string_manipulation_ins = ['MOVS']
        flag_manipulation_ins = ['STC']
        stack_related_ins = ['PUSH', 'POP', 'PUSHF', 'POPF']
        input_output_ins = ['IN', 'OUT']
        miscellaneous_ins = ['NOP', 'INT', 'HLT']


        if self.opcode in data_transfer_ins:
            self.data_transfer_ins()
        elif self.opcode in arithmetic_ins:
            self.arithmetic_ins()
        elif self.opcode in logical_ins:
            self.logical_ins()
        elif self.opcode in rotate_shift_ins:
            self.rotate_shift_ins()
        elif self.opcode in transfer_control_ins:
            self.transfer_control_ins()
        elif self.opcode in string_manipulation_ins:
            self.string_manipulation_ins()
        elif self.opcode in flag_manipulation_ins:
            self.flag_manipulation_ins()
        elif self.opcode in stack_related_ins:
            self.stack_related_ins()
        elif self.opcode in input_output_ins:
            self.input_output_ins()
        elif self.opcode in miscellaneous_ins:
            self.miscellaneous_ins()
        else:
            sys.exit("operation code not support")

    def data_transfer_ins(self):
        if self.opcode == 'MOV':
            result = self.eo[1]
            if self.oprands[0] in self.GR.list:
                self.GR.write(self.oprands[0], result)
            elif '[' in self.oprands[0]:
                location = self.oprands[0].replace('[', '').replace(']', '')
                self.bus.write_cache(location, result)
        elif self.opcode == 'XCHG':
            pass
        elif self.opcode == 'LEA':
            pass
        elif self.opcode == 'LDS':
            pass
        elif self.opcode == 'LES':
            pass
        else:
            pass        

    def arithmetic_ins(self):
        if self.opcode == 'ADD':
            result = self.eo[0] + self.eo[1]
            self.GR.write(self.oprands[0], result)

        elif self.opcode == 'SUB':
            result = self.eo[0] - self.eo[1]
            self.GR.write(self.oprands[0], result)

        elif self.opcode == 'MUL': 
            result = self.eo[0] * self.GR.read_int('AX')
            self.GR.write('AX', result)

        elif self.opcode == 'DIV':
            divisor = self.eo[0]
            divident = int(self.GR.read('AX'))
            quotient = divident // divisor
            remainder = divident % divisor
            self.GR.write('AX', quotient)
            self.GR.write('DX', remainder)
        
        elif self.opcode == 'INC':
            result = self.eo[0] + 1
            self.GR.write(self.oprands[0], result)

        elif self.opcode == 'DEC':
            result = self.eo[0] - 1
            self.GR.write(self.oprands[0], result)

        else:
            sys.exit("operation code not support")


    def logical_ins(self):
        pass

    def rotate_shift_ins(self):
        pass

    def transfer_control_ins(self):
        if self.opcode == 'JMP':
            self.bus.IP = self.eo[0]
        else:
            pass

    def string_manipulation_ins(self):
        pass

    def flag_manipulation_ins(self):
        pass

    def stack_related_ins(self):
        pass

    def input_output_ins(self):
        pass

    def miscellaneous_ins(self):
        pass