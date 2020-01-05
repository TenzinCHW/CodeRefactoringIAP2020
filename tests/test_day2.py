import pytest
from src.day2 import IntcodeComputer, InvalidOpException

def test_add():
    instructions = [1, 4, 3, 3,
            99]
    expected = [1, 4, 3, 102,
            99]
    actual_eq_expected(instructions, expected)

def test_mult():
    instructions = [2, 2, 3, 3,
            99]
    expected = [2, 2, 3, 9,
            99]
    actual_eq_expected(instructions, expected)

def test_multiple_instructions():
    instructions = [1, 9, 10, 3,
            2, 3, 11, 0,
            99,
            30, 40, 50]
    expected = [3500, 9, 10, 70,
            2, 3, 11, 0,
            99,
            30, 40, 50]
    actual_eq_expected(instructions, expected)
    instructions = [1,1,1,4,
            99,
            5,6,0,
            99]
    expected = [30,1,1,4,
            2,5,6,0,
            99]
    actual_eq_expected(instructions, expected)

@pytest.mark.xfail(raises=InvalidOpException)
def test_fail():
    instructions = [0, 0, 0, 0]
    run_instructions(instructions)

def actual_eq_expected(instructions, expected):
    actual = run_instructions(instructions)
    assert(actual == expected)

def run_instructions(instructions):
    icc = IntcodeComputer(instructions)
    return icc.run()

