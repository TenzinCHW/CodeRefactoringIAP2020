import pytest
from src.day2 import IntcodeComputer, InvalidOpException

def test_add():
    instructions = [1, 4, 3, 3, 99]
    expected = [1, 4, 3, 102, 99]
    actual_eq_expected(instructions, expected)

def test_mult():
    instructions = [2, 2, 3, 3, 99]
    expected = [2, 2, 3, 9, 99]
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

