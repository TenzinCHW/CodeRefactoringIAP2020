import pytest
from src.day7 import IntcodeComputer, InvalidOpException, AmplifierCircuit

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

def test_thruster():
    instructions = ([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
            [3,23,3,24,1002,24,10,24,1002,23,-1,23,
                101,5,23,23,1,24,23,23,4,23,99,0,0],
            [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,
                1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
    max_thrust_setting = ((43210, 43210),
            (54321, 1234),
            (65210, 10432))
    for instr, ts in zip(instructions, max_thrust_setting):
        expected_thrust, expected_setting = ts
        ac = AmplifierCircuit(5, instr)
        max_thrust, max_setting = ac.get_max_thruster_setting()
        assert max_thrust == expected_thrust
        assert max_setting == expected_setting

def actual_eq_expected(instructions, expected):
    icc = run_instructions(instructions)
    actual = icc.memory
    assert actual == expected

def check_output(instructions, inp, expected_out):
    icc = run_instructions(instructions, inp=inp)
    actual_out = icc.out[-1]
    assert actual_out == expected_out

def run_instructions(instructions, inp=None):
    icc = IntcodeComputer(instructions)
    icc.run(inp=inp)
    return icc

