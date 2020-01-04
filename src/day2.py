class IntcodeComputer:
    def __init__(self, instructions):
        self.memory = instructions

    def run(self):
        num_instructions = len(self.memory) // 4
        for i in range(num_instructions):
            instruction = self.memory[i:i+4]
            try:
                self.exec(instruction)
            except HaltException:
                break
        return self.memory

    def exec(self, instruction):
        op, arg1_loc, arg2_loc, out_loc = instruction
        arg1, arg2 = map(self.mem_load, (arg1_loc, arg2_loc))
        if op == 1:
            out = arg1 + arg2
        elif op == 2:
            out = arg1 * arg2
        elif op == 99:
            raise HaltException
        else:
            raise InvalidOpException
        self.mem_store(out_loc, out)

    def mem_load(self, mem_loc):
        return self.memory[mem_loc]

    def mem_store(self, mem_loc, value):
        self.memory[mem_loc] = value

class HaltException(Exception):
    pass

class InvalidOpException(Exception):
    pass

