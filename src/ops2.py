class HaltException(Exception):
    pass

class InvalidOpException(Exception):
    pass

def plus(a, b):
    return a + b

def mult(a, b):
    return a * b

def halt(): # Dummy function
    pass

HALT_CODE = 99

ops = {1 : plus,
        2 : mult,
        99: halt}

