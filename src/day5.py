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
        if op == HALT_CODE:
            raise HaltException
        elif op in OPS:
            self.exec(op, argmodes)
        else:
            raise InvalidOpException

    def exec(self, op, argmodes):
        num_args = OPS_NUM_ARGS[op]
        args = self.memory[self.pc+1:self.pc+1+num_args]
        if op == 1:
            self.two_arg_store(*args, argmodes, add)
        elif op == 2:
            self.two_arg_store(*args, argmodes, mult)
        elif op == 3:
            self.mem_store(*args, self.inp)
        elif op == 4:
            self.out = self.mem_load(*args)
        elif op == 5:
            self.jump(*args, argmodes, neq_zero)
        elif op == 6:
            self.jump(*args, argmodes, eq_zero)
        elif op == 7:
            self.two_arg_store(*args, argmodes, lt)
        elif op == 8:
            self.two_arg_store(*args, argmodes, eq)
        self.pc += 1 + num_args

    def arg_values(self, argmodes, *args):
        decoded_args = []
        for i, arg in enumerate(args):
            if (argmodes // 10 ** i) % (10 ** (i+1)) == 0:
                decoded_args.append(self.mem_load(arg))
            else:
                decoded_args.append(arg)
        return decoded_args

    def jump(self, a_loc, b_loc, argmodes, decision_func):
        a, b = self.arg_values(argmodes, a_loc, b_loc)
        self.pc = decision_func(a, b, self.pc)

    def two_arg_store(self, a_loc, b_loc, loc, argmodes, func):
        a, b = self.arg_values(argmodes, a_loc, b_loc)
        self.mem_store(loc, func(a, b))

    def mem_load(self, mem_loc):
        self.check_mem_inbound(mem_loc)
        return self.memory[mem_loc]

    def mem_store(self, mem_loc, value):
        self.check_mem_inbound(mem_loc)
        self.memory[mem_loc] = value

    def check_mem_inbound(self, mem_loc):
        if mem_loc < 0 or mem_loc >= len(self.memory):
            print('memory location {mem_loc} is out bounds')

