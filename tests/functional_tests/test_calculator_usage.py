import pytest
from astropy import units as u
from atlast_sc.calculator import Calculator

# TODO: test some use cases


class TestCalculatorUsage:

    def test_use_calculator_with_defaults(self, t_int, sensitivity, obs_freq,
                                          t_atm, calculator):

        # Create a new calculator object using the default parameters
        test_calculator = Calculator()

        # Calculate the sensitivity using default parameters
        sens = test_calculator.calculate_sensitivity()

        # Verify that the calculator now stores the newly calculated
        # sensitivity
        assert sens == test_calculator.sensitivity
        # Verify that the sensitivity is about 2.97 mJy
        assert test_calculator.sensitivity.value == pytest.approx(2.97, 0.01)
        assert test_calculator.sensitivity.unit == u.mJy

        # Update observing frequency
        test_calculator.obs_freq = 850 * u.GHz

        # Verify that the observing frequency has been updated
        assert test_calculator.obs_freq != obs_freq
        # Verify that other parameters that depend on the observing frequency
        # have been updated (just testing one here; full tests are performed
        # elsewhere)
        assert test_calculator.T_atm != t_atm

        # Recalculate the sensitivity
        new_sens = test_calculator.calculate_sensitivity()
        # Verify that the new sensitivity differs from the previous value
        assert new_sens != sens

        # Calculate sensitivity using a different integration time, but don't
        # update the calculator with the new calculated value
        test_t_int = 3 * u.h
        sens = test_calculator.calculate_sensitivity(test_t_int,
                                                     update_calculator=False)
        # Verify that the calculator has been updated with the new integration
        # time
        assert test_calculator.t_int == test_t_int
        # Verify that the sensitivity has not been updated
        assert test_calculator.sensitivity != sens

        # Reset the calculator
        test_calculator.reset()
        # Verify that the calculator has now been reset to its initial state
        assert test_calculator.calculation_inputs == \
               calculator.calculation_inputs
        assert test_calculator.derived_parameters == \
               calculator.derived_parameters

        # Calculate the integration time with default values
        new_t_int = test_calculator.calculate_t_integration()
        # Verify that the calculator has been updated with calculated
        # integration time
        assert test_calculator.t_int == new_t_int
        # Verify that the calculated integration time is about 100 s
        assert test_calculator.t_int.value == pytest.approx(100, 3)
        assert test_calculator.t_int.unit == u.s

    def test_calculator_from_file(self):
        pass
