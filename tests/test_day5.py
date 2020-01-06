import pytest
from src.day5 import IntcodeComputer, InvalidOpException

def test_add():
    instructions = [1,4,3,3,99]
    expected = [1,4,3,102,99]
    actual_eq_expected(instructions, expected)
    instructions = [1101,4,3,3,99]
    expected = [1101,4,3,7,99]
    actual_eq_expected(instructions, expected)

def test_mult():
    instructions = [2,2,3,3,99]
    expected = [2,2,3,9,99]
    actual_eq_expected(instructions, expected)
    instructions = [1102,2,3,3,99]
    expected = [1102,2,3,6,99]
    actual_eq_expected(instructions, expected)

def test_multiple_instructions():
    instructions = [1,9,10,3,2,3,11,0,99,30,40,50]
    expected = [3500,9,10,70,2,3,11,0,99,30,40,50]
    actual_eq_expected(instructions, expected)
    instructions = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    actual_eq_expected(instructions, expected)

def test_immediate_mode():
    instructions = [1002,4,3,4,33]
    expected = [1002,4,3,4,3*33]
    actual_eq_expected(instructions, expected)

def test_input_output():
    instructions = [3,0,4,0,99]
    inp = (20,)
    expected_out = 20
    check_output(instructions, inp, expected_out)

def test_eq_8():
    instructions = [3,9,8,9,10,9,4,9,99,-1,8]
    inp = (8,)
    expected_out = 1
    check_output(instructions, inp, expected_out)
    instructions = [3,3,1108,-1,8,3,4,3,99]
    check_output(instructions, inp, expected_out)

def test_neq_8():
    instructions = [3,9,8,9,10,9,4,9,99,-1,8]
    not_8 = (7,)
    expected_out = 0
    check_output(instructions, not_8, expected_out)
    instructions = [3,3,1108,-1,8,3,4,3,99]
    check_output(instructions, not_8, expected_out)

def test_lt_8():
    instructions = [3,9,7,9,10,9,4,9,99,-1,8]
    lt_8 = (7,)
    expected_out = 1
    check_output(instructions, lt_8, expected_out)
    instructions = [3,3,1107,-1,8,3,4,3,99]
    check_output(instructions, lt_8, expected_out)

def test_jmp_eq0():
    instructions = [1105,1,5,4,1,4,0,99]
    expected_out = 1105
    check_output(instructions, None, expected_out)

def test_jmp_neq0():
    instructions = [1106,0,5,4,1,4,0,99]
    expected_out = 1106
    check_output(instructions, None, expected_out)

def test_dont_jmp_eq0():
    instructions = [1105,0,6,4,0,99,4,1,99]
    expected_out = 1105
    check_output(instructions, None, expected_out)

def test_dont_jmp_neq0():
    instructions = [1106,1,6,4,0,99,4,1,99]
    expected_out = 1106
    check_output(instructions, None, expected_out)

@pytest.mark.xfail(raises=InvalidOpException)
def test_fail():
    instructions = [0,0,0,0]
    run_instructions(instructions)

def actual_eq_expected(instructions, expected):
    icc = run_instructions(instructions)
    actual = icc.memory
    assert actual == expected

def check_output(instructions, inp, expected_out):
    icc = run_instructions(instructions, inp=inp)
    actual_out = icc.out
    assert actual_out == expected_out

def run_instructions(instructions, inp=None):
    icc = IntcodeComputer(instructions)
    icc.run(inp=inp)
    return icc

