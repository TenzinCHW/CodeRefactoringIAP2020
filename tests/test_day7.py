import pytest
from src.day7 import IntcodeComputer, InvalidOpException, AmplifierCircuit

def test_add():
    instructions = [1,4,3,3,99]
    expected = [1,4,3,102,99]
    actual_eq_expected(instructions, expected)

def test_mult():
    instructions = [2,2,3,3,99]
    expected = [2,2,3,9,99]
    actual_eq_expected(instructions, expected)

def test_multiple_instructions():
    instructions = [1,9,10,3,2,3,11,0,99,30,40,50]
    expected = [3500,9,10,70,2,3,11,0,99,30,40,50]
    actual_eq_expected(instructions, expected)
    instructions = [1,1,1,4,99,5,6,0,99]
    expected = [30,1,1,4,2,5,6,0,99]
    actual_eq_expected(instructions, expected)

def test_immediate_mode():
    instructions = [1002, 4, 3, 4, 33]
    expected = [1002, 4, 3, 4, 3*33]
    actual_eq_expected(instructions, expected)

def test_input_output():
    instructions = [3, 0, 4, 0 ,99]
    icc = IntcodeComputer(instructions)
    icc.run((20,))
    assert(icc.out == 20)

@pytest.mark.xfail(raises=InvalidOpException)
def test_fail():
    instructions = [0, 0, 0, 0]
    run_instructions(instructions)

def test_thruster():
    instructions = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    ac = AmplifierCircuit(5, instructions)
    max_thrust, max_setting = ac.get_max_thruster_setting()
    assert(max_thrust == 43210)
    assert(max_setting == 43210)

def actual_eq_expected(instructions, expected):
    actual = run_instructions(instructions)
    assert(actual == expected)

def run_instructions(instructions):
    icc = IntcodeComputer(instructions)
    return icc.run()

