from pathlib import Path
import pytest
import astropy.units as u
from atlast_sc.calculator import Calculator
from atlast_sc.config import Config

CONFIG_PATH = Path(__file__).resolve().parents[0]

config = Config.from_yaml(CONFIG_PATH, "test_user_inputs.yaml")

calculator = Calculator(config)


def test_sensitivity():
    # This assert statement is currently failing due to the static value being incorrect.
    # These values should be re-calculated by hand to ensure tests are correct and robust.
    assert calculator.sensitivity(config.t_int).value == pytest.approx(0.007675, abs=0.00001)


def test_integration():
    # This assert statement is currently failing due to the static value being incorrect.
    # These values should be re-calculated by hand to ensure tests are correct and robust.
    assert calculator.t_integration(config.sensitivity).value == pytest.approx(0.5892, abs=0.0001)


def test_consistency():
    t = calculator.t_integration(config.sensitivity)
    assert calculator.sensitivity(t).to(u.mJy).value == pytest.approx(config.sensitivity.to(u.mJy).value, abs=0.01)