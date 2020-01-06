class HaltException(Exception):
    pass

class InvalidOpException(Exception):
    pass

HALT_CODE = 99

OPS_NUM_ARGS = {1 : 3,
        2 : 3,
        3 : 1,
        4 : 1,
        5 : 2,
        6 : 2,
        7 : 3,
        8 : 3}

def add(a, b):
    return a + b

def mult(a, b):
    return a * b

def neq_zero(a, b, c):
    if a != 0:
        return b
    return c

def eq_zero(a, b, c):
    if a == 0:
        return b
    return c

def lt(a, b):
    return int(a < b)

def eq(a, b):
    return int(a == b)

