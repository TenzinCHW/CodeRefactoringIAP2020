from multiprocessing import Queue
from copy import copy
from itertools import permutations
from threading import Thread
try:
    from src.ops7 import *
except:
    from ops7 import *

class IntcodeComputer:
    def __init__(self, instructions):
        self.instructions = copy(instructions)
        self.memory = copy(instructions)
        self.in_q = Queue()
        self.out_q = Queue()

    def reinit(self):
        self.memory = copy(self.instructions)
        while not self.in_q.empty():
            self.in_q.get_nowait()
        while not self.out_q.empty():
            self.out_q.get_nowait()

    def start(self):
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.thread.join()

    def send(self, value):
        self.in_q.put(value)

    def receive(self):
        return self.out_q.get()

    def run(self):
        pc = 0
        while pc < len(self.memory):
            try:
                pc = self.try_exec(pc)
            except HaltException:
                break

    def try_exec(self, pc):#argmodes, pc, inp=None):
        opcode = self.memory[pc]
        argmodes, op = opcode // 100, opcode % 100
        ops = OPS_NUM_ARGS.keys()
        if op == HALT_CODE:
            raise HaltException
        elif op in ops:
            return self.exec(op, argmodes, pc)
        else:
            raise InvalidOpException

    def exec(self, op, argmodes, pc):
        num_args = OPS_NUM_ARGS[op]
        args = self.memory[pc+1:pc+1+num_args]
        pc += 1 + num_args
        if op == 1:
            self.two_arg_store(*args, argmodes, add)
        elif op == 2:
            self.two_arg_store(*args, argmodes, mult)
        elif op == 3:
            try:
                inp = self.in_q.get()
            except OSError as e:
                raise e
            self.mem_store(*args, inp)
        elif op == 4:
            out = self.mem_load(*args)
            try:
                self.out_q.put(out)
            except OSError as e:
                raise e
        elif op == 5:
            pc = self.jump(*args, argmodes, pc, neq_zero)
        elif op == 6:
            pc = self.jump(*args, argmodes, pc, eq_zero)
        elif op == 7:
            self.two_arg_store(*args, argmodes, lt)
        elif op == 8:
            self.two_arg_store(*args, argmodes, eq)
        return pc

    def arg_values(self, argmodes, *args):
        decoded_args = []
        for i, arg in enumerate(args):
            argmode = argmodes // 10 ** i
            if argmode % 10 == 0:
                value = self.mem_load(arg)
                decoded_args.append(value)
            elif argmode % 10 == 1:
                decoded_args.append(arg)
            else:
                raise InvalidParameterModeException
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
        assert type(value) == int, 'value being stored must be an int'
        self.memory[mem_loc] = value

    def check_mem_inbound(self, mem_loc):
        if mem_loc < 0 or mem_loc >= len(self.memory):
            print('memory location {mem_loc} is out bounds')

class AmplifierCircuit:
    def __init__(self, num_thrusters, instructions, start_settings=0):
        self.iccs = [IntcodeComputer(instructions)
                for _ in range(num_thrusters)]
        settings = ''.join(str(i) for i in range(start_settings, start_settings + num_thrusters))
        self.possible_settings = permutations(settings)

    def reinit_iccs(self):
        for icc in self.iccs:
            icc.reinit()

    def get_max_thruster_setting(self, run_method):
        max_thrust = 0  # TODO check if this is really the smallest
        for setting in self.possible_settings:
            amp_out = run_method(setting)
            if amp_out > max_thrust:
                max_thrust = amp_out
                max_setting = int(''.join(setting))

            # Reset memory of all computers
            self.reinit_iccs()
        return max_thrust, max_setting

    def run_sequentially(self, setting):
        inp = 0
        for i, icc in enumerate(self.iccs):
            icc.start()
            icc.send(int(setting[i]))
            icc.send(inp)
            inp = icc.receive()
            icc.stop()
        return inp

    def run_loop(self, setting):
        for i, icc in enumerate(self.iccs):
            icc.in_q = self.iccs[i-1].out_q
        for s, icc in zip(setting, self.iccs):
            icc.send(int(s))
        self.iccs[0].send(0)
        for icc in self.iccs:
            icc.start()
        for icc in self.iccs:
            icc.stop()
        while not self.iccs[-1].out_q.empty():
            amp_out = self.iccs[-1].receive()
        return amp_out

