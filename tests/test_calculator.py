from pathlib import Path
import pytest
import astropy.units as u
from atlast_sc.calculator import Calculator
from atlast_sc.utils import FileHelper

CONFIG_PATH = Path(__file__).resolve().parents[0]

user_input = FileHelper.read_from_file(CONFIG_PATH, "test_user_inputs.yaml")

calculator = Calculator(user_input)


def test_sensitivity():
    # TODO: These values should be re-calculated by hand to ensure
    #  tests are correct and robust.
    assert calculator.calculate_sensitivity(calculator.t_int).value \
           == pytest.approx(0.0057, abs=0.00001)


def test_integration():
    # TODO: These values should be re-calculated by hand to ensure
    #  tests are correct and robust.
    assert calculator.calculate_t_integration(calculator.sensitivity).value \
           == pytest.approx(0.32536, abs=0.0001)


def test_consistency():
    t = calculator.calculate_t_integration(calculator.sensitivity)
    assert calculator.calculate_sensitivity(t).to(u.mJy).value == \
           pytest.approx(calculator.sensitivity.to(u.mJy).value, abs=0.01)
