import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator

    def test_multiply_calculate_correct(self):
        assert self.calc.multiply(self, 2, 2) == 4

    def test_multiply_calculate_faled(self):
        assert self.calc.multiply(self, 2, 2) == 5

    def test_multiply_calculate_correct2(self):
        assert self.calc.multiply(self, 3, 3) == 9

    def test_division_calculate_correct(self):
        assert self.calc.division(self, 3, 3) == 1.0

    def test_subtraction_calculate_correct(self):
        assert self.calc.subtraction(self, 7, 3) == 4

    def test_adding_calculate_correct(self):
        assert self.calc.adding(self, 7, 3) == 10