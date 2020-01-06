from copy import copy
try:
    from src.ops5 import *
except:
    from ops5 import *

class IntcodeComputer:
    def __init__(self, instructions):
        self.memory = copy(instructions)

    def run(self, inp=None):
        self.inp = inp
        inp_ptr = 0
        pc = 0
        while pc < len(self.memory):
            try:
                pc, inp_ptr = self.try_exec(pc, inp_ptr)
            except HaltException:
                break
        return self.memory

    def try_exec(self, pc, inp_ptr):
        opcode = self.memory[pc]
        ops = OPS_NUM_ARGS.keys()
        argmodes, op = opcode // 100, opcode % 100
        if op == HALT_CODE:
            raise HaltException
        elif op in ops:
            return self.exec(op, argmodes, pc, inp_ptr)
        else:
            raise InvalidOpException

    def exec(self, op, argmodes, pc, inp_ptr):
        num_args = OPS_NUM_ARGS[op]
        args = self.memory[pc+1:pc+1+num_args]
        pc += 1 + num_args
        if op == 1:
            self.two_arg_store(*args, argmodes, add)
        elif op == 2:
            self.two_arg_store(*args, argmodes, mult)
        elif op == 3:
            inp = self.inp[inp_ptr]
            inp_ptr += 1
            self.mem_store(*args, inp)
        elif op == 4:
            self.out = self.mem_load(*args)
        elif op == 5:
            pc = self.jump(*args, argmodes, pc, neq_zero)
        elif op == 6:
            pc = self.jump(*args, argmodes, pc, eq_zero)
        elif op == 7:
            self.two_arg_store(*args, argmodes, lt)
        elif op == 8:
            self.two_arg_store(*args, argmodes, eq)
        return pc, inp_ptr

    def arg_values(self, argmodes, *args):
        decoded_args = []
        for i, arg in enumerate(args):
            argmode = argmodes // 10 ** i
            if argmode % 10 == 0:
                value = self.mem_load(arg)
                decoded_args.append(value)
            else:
                decoded_args.append(arg)
        return decoded_args

    def jump(self, a_loc, b_loc, argmodes, pc, jump_to):
        a, b = self.arg_values(argmodes, a_loc, b_loc)
        return jump_to(a, b, pc)

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

