from src.ops5 import *

class IntcodeComputer:
    def __init__(self, instructions):
        self.memory = instructions
        self.pc = 0

    def run(self, inp=None):
        self.inp = inp
        while self.pc < len(self.memory):
            try:
                self.try_exec()
            except HaltException:
                break
        return self.memory

    def try_exec(self):
        opcode = self.memory[self.pc]
        argmodes, op = opcode // 100, opcode % 100
        ops = self.ops()
        if op == HALT_CODE:
            raise HaltException
        if op in ops.keys():
            self.exec(op, ops, argmodes)
        else:
            raise InvalidOpException

    def ops(self):
        return {1 : (self.plus, 3),
                2 : (self.mult, 3),
                3 : (self.input, 1),
                4 : (self.output, 1)}

    def exec(self, op, ops, argmodes):
        func, num_args = ops[op]
        args = self.memory[self.pc+1:self.pc+1+num_args]
        func(*args, argmodes)
        self.pc += 1 + num_args

    def arg_values(self, argmodes, *args):
        decoded_args = []
        for i, arg in enumerate(args):
            if (argmodes // 10 ** i) % (10 ** (i+1)) == 0:
                decoded_args.append(self.mem_load(arg))
            else:
                decoded_args.append(arg)
        return decoded_args

    def plus(self, a_loc, b_loc, loc, argmodes):
        a, b = self.arg_values(argmodes, a_loc, b_loc)
        self.mem_store(loc, a + b)

    def mult(self, a_loc, b_loc, loc, argmodes):
        a, b = self.arg_values(argmodes, a_loc, b_loc)
        self.mem_store(loc, a * b)

    def input(self, loc, argmode):
        self.mem_store(loc, self.inp)

    def output(self, loc, argmode):
        self.out = self.mem_load(loc)

    def mem_load(self, mem_loc):
        self.check_mem_inbound(mem_loc)
        return self.memory[mem_loc]

    def mem_store(self, mem_loc, value):
        self.check_mem_inbound(mem_loc)
        self.memory[mem_loc] = value

    def check_mem_inbound(self, mem_loc):
        if mem_loc < 0 or mem_loc >= len(self.memory):
            print('memory location {mem_loc} is out bounds')

