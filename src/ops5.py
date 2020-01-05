class HaltException(Exception):
    pass

class InvalidOpException(Exception):
    pass

HALT_CODE = 99

OPS = (1, 2, 3, 4)

OPS_NUM_ARGS = {1 : 3,
        2 : 3,
        3 : 1,
        4 : 1}

def add(a, b):
    return a + b

def mult(a, b):
    return a * b

