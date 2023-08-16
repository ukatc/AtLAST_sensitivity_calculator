import pytest
from astropy import units as u
from atlast_sc.calculator import Calculator
from atlast_sc.utils import FileHelper


class TestCalculatorUsage:

    def test_use_calculator_with_defaults(self, calculator):

        # Create a new calculator object using the default parameters
        test_calculator = Calculator()

        # Calculate the sensitivity using default parameters
        sens = test_calculator.calculate_sensitivity().to(u.mJy)

        # Verify that the calculator now stores the newly calculated
        # sensitivity
        assert sens == test_calculator.sensitivity
        # Verify that the sensitivity is about 0.78 mJy
        assert test_calculator.sensitivity.value == pytest.approx(0.78, 0.01)
        assert test_calculator.sensitivity.unit == u.mJy

        # Update observing frequency
        test_calculator.obs_freq = 850 * u.GHz
        # Verify that other parameters that depend on the observing frequency
        # have been updated
        assert test_calculator.derived_parameters \
               != calculator.derived_parameters

        # Recalculate the sensitivity
        new_sens = test_calculator.calculate_sensitivity()
        # Verify that the new sensitivity differs from the previous value
        assert new_sens != sens

        # Calculate sensitivity using a different integration time
        test_t_int = 3 * u.h
        test_calculator.calculate_sensitivity(test_t_int)
        # Verify that the integration time has been updated
        assert test_calculator.t_int == test_t_int

        # Calculate sensitivity using a different integration time, but don't
        # update the calculator
        test_t_int = 3 * u.min
        sens = test_calculator.calculate_sensitivity(test_t_int,
                                                     update_calculator=False)
        # Verify that integration time has not been updated
        assert test_calculator.t_int != test_t_int
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
        new_t_int = test_calculator.calculate_t_integration().to(u.s)
        # Verify that the calculator has been updated with calculated
        # integration time
        assert test_calculator.t_int == new_t_int
        # Verify that the calculated integration time is about 100 s
        assert test_calculator.t_int.value == pytest.approx(100, 3)
        assert test_calculator.t_int.unit == u.s

        # Calculate integration time using a different sensitivity
        test_sens = 300 * u.mJy
        test_calculator.calculate_t_integration(test_sens)
        # Verify that the sensitivity has been updated
        assert test_calculator.sensitivity == test_sens
        # Calculate integration time using a different sensitivity, but don't
        # update the calculator
        test_sens = 30 * u.mJy
        t_int = \
            test_calculator.calculate_t_integration(test_sens,
                                                    update_calculator=False)
        # Verify that the sensitivity has not been updated
        assert test_calculator.sensitivity != test_sens
        # Verify that the integration time has not been updated
        assert test_calculator.t_int != t_int

    def test_calculator_from_to_files(self, test_files_path, tmp_output_dir):

        # Read user input from a file and initialize the calculator with the
        # result
        user_input = FileHelper.read_from_file(test_files_path,
                                               'user_input.yaml')
        test_calculator = Calculator(user_input)

        # Verify that the calculator has been initialized with the correct
        # user input
        assert test_calculator.t_int == 150 * u.s
        assert test_calculator.sensitivity == 30 * u.mJy
        assert test_calculator.bandwidth == 150 * u.MHz
        assert test_calculator.obs_freq == 200 * u.GHz
        assert test_calculator.n_pol == 1
        assert test_calculator.weather == 30
        assert test_calculator.elevation == 65 * u.deg

        # Update the observing frequency
        test_calculator.obs_freq = 850 * u.GHz

        # Calculate the sensitivity
        test_calculator.calculate_sensitivity()

        # Write the results to a file
        FileHelper.write_to_file(test_calculator, tmp_output_dir,
                                 'calculator_output', 'yaml')

        # Verify that the output file contains the expected list of
        # parameters
        expected_params = ['t_int', 'sensitivity', 'bandwidth', 'n_pol',
                           'obs_freq', 'weather', 'elevation', 'tau_atm',
                           'T_atm', 'T_rx', 'eta_a', 'eta_s', 'T_sys', 'T_sky',
                           'sefd']
        # sort the expected parameters
        expected_params.sort()

        output_dict = \
            FileHelper.read_from_file(tmp_output_dir, 'calculator_output.yaml')
        # list and sort the output dictionary keys
        result_dict_keys = list(output_dict.keys())
        result_dict_keys.sort()

        assert result_dict_keys == expected_params
