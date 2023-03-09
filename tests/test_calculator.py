import pytest
import astropy.units as u
from atlast_sc.calculator import Calculator


class TestCalculator:

    @staticmethod
    @pytest.fixture
    def calculator(user_input_params):
        return Calculator(user_input_params)

    def test_sensitivity(self, calculator):
        # TODO: These values should be re-calculated by hand to ensure
        #  tests are correct and robust.

        assert calculator.calculate_sensitivity(calculator.t_int).value \
               == pytest.approx(0.0057, abs=0.00001)

    def test_integration(self, calculator):
        # TODO: These values should be re-calculated by hand to ensure
        #  tests are correct and robust.
        assert calculator.calculate_t_integration(calculator.sensitivity)\
                   .value \
               == pytest.approx(0.32536, abs=0.0001)

    def test_consistency(self, calculator):
        t = calculator.calculate_t_integration(calculator.sensitivity)
        assert calculator.calculate_sensitivity(t).to(u.mJy).value == \
               pytest.approx(calculator.sensitivity.to(u.mJy).value, abs=0.01)
