import pytest
import astropy.units as u
from atlast_sc.calculator import Calculator
from atlast_sc.models import DerivedParams, CalculationInput

# TODO: This is WIP


class TestCalculator:

    init_calc_input = [
        ({}, 'default', 'Default values used'),
        ({'t_int': {'value': 1, 'unit': 's'},
          'bandwidth': {'value': 10, 'unit': 'MHz'},
          }, 'custom',
         'Custom values and defaults for remainder used'
         )
    ]

    @pytest.mark.parametrize('input_data,expected_data,scenario',
                             init_calc_input)
    def test_initialize_calculator(self, input_data, expected_data, scenario,
                                   mocker):

        print('testing scenario:', scenario)
        derived_params_spy = \
            mocker.spy(Calculator,
                       '_calculate_derived_parameters')

        # Initialize the calculator
        calculator = Calculator(input_data)

        # Make sure the derived parameters were calculated
        derived_params_spy.assert_called_once()

        # Make sure calculator contains a config object with
        # calculation inputs, and a derived params object
        assert isinstance(calculator._config.calculation_inputs,
                          CalculationInput)
        assert isinstance(calculator._derived_params, DerivedParams)

        # # Check that the calculator has been configured with the correct
        # # input data

    # TODO test invalid input parameters result in an error

    # def test_sensitivity(self, calculator):
    #     # TODO: These values should be re-calculated by hand to ensure
    #     #  tests are correct and robust.
    #
    #     assert calculator.calculate_sensitivity(calculator.t_int).value \
    #            == pytest.approx(0.0057, abs=0.00001)
    #
    # def test_integration(self, calculator):
    #     # TODO: These values should be re-calculated by hand to ensure
    #     #  tests are correct and robust.
    #     assert calculator.calculate_t_integration(calculator.sensitivity)\
    #                .value \
    #            == pytest.approx(0.32536, abs=0.0001)

    def test_consistency(self, calculator):
        t = calculator.calculate_t_integration(calculator.sensitivity)
        assert calculator.calculate_sensitivity(t).to(u.mJy).value == \
               pytest.approx(calculator.sensitivity.to(u.mJy).value, abs=0.01)
