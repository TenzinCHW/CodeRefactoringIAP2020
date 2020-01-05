from itertools import permutations
from src.ops7 import *

class IntcodeComputer:
    def __init__(self, instructions):
        self.memory = instructions
        self.instructions = instructions
        self.pc = 0
        self.input_ptr = 0

    def reinit(self):
        self.memory = self.instructions
        self.pc = 0
        self.input_ptr = 0

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
        if op in OPS:
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
            inp = self.inp[self.input_ptr]
            self.mem_store(*args, inp)
            self.input_ptr += 1
        else: #4
            self.out = self.mem_load(*args)
        self.pc += 1 + num_args

    def arg_values(self, argmodes, *args):
        decoded_args = []
        for i, arg in enumerate(args):
            if (argmodes // 10 ** i) % (10 ** (i+1)) == 0:
                decoded_args.append(self.mem_load(arg))
            else:
                decoded_args.append(arg)
        return decoded_args

    def two_arg_store(self, a_loc, b_loc, loc, argmodes, func):
        a, b = self.arg_values(argmodes, a_loc, b_loc)
        self.mem_store(loc, func(a, b))

    def mem_load(self, mem_loc):
        self.check_mem_inbound(mem_loc)
        return self.memory[mem_loc]

    def mem_store(self, mem_loc, value):
        self.check_mem_inbound(mem_loc)
        assert type(value) == int, 'value must be an int'
        self.memory[mem_loc] = value

    def check_mem_inbound(self, mem_loc):
        if mem_loc < 0 or mem_loc >= len(self.memory):
            print('memory location {mem_loc} is out bounds')

class AmplifierCircuit:
    def __init__(self, num_thrusters, instructions):
        self.iccs = [IntcodeComputer(instructions)
                for _ in range(num_thrusters)]
        settings = ''.join(str(i) for i in range(num_thrusters))
        self.possible_settings = permutations(settings)

    def get_max_thruster_setting(self):
        max_thrust = 0  # TODO check if this is really the smallest
        for setting in self.possible_settings:
            inp = 0
            for i, icc in enumerate(self.iccs):
                icc.run(inp=(int(setting[i]), inp))
                inp = icc.out
                icc.reinit()

            if self.iccs[-1].out > max_thrust:
                max_thrust = self.iccs[-1].out
                max_setting = int(''.join(setting))
        return max_thrust, max_setting

