import pytest
import astropy.units as u
import atlast_sc.calculator as sc
from atlast_sc.models import DerivedParams, CalculationInput


# class DataHelper:
#
#     @staticmethod
#     @pytest.fixture(scope='session')
#     def default_user_input(user_input_params):
#         return user_input_params
#
#     @staticmethod
#     def get_default_input(default_user_input):
#         return default_user_input()


class TestCalculator:

    @staticmethod
    @pytest.fixture
    def calculator(user_input_params):
        return sc.Calculator(user_input_params)

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
                                   user_input_params, mocker):

        print('testing scenario:', scenario)
        derived_params_spy = \
            mocker.spy(sc.Calculator,
                       '_calculate_derived_parameters')

        # Initialize the calculator
        calculator = sc.Calculator(input_data)

        # Make sure the derived parameters were calculated
        derived_params_spy.assert_called_once()

        # Make sure calculator contains a config object with
        # calculation inputs, and a derived params object
        assert isinstance(calculator._config.calculation_inputs,
                          CalculationInput)
        assert isinstance(calculator._derived_params, DerivedParams)

        # TODO: pick up from here
        # # Check that the calculator has been configured with the correct
        # # input data
        # # Have to construct the expected parameters inside this func
        # # if we want to make use of fixtures
        # expected_configured_params = {}
        # if expected_data == 'default':
        #     expected_configured_params = user_input_params
        # else:
        #     for param in user_input_params:
        #         if param in input_data:
        #             expected_configured_params[param] = input_data[param]
        #         else:
        #             expected_configured_params[param] = \
        #                 user_input_params[param]
        # calculator_params = calculator.calculation_parameters_as_dict
        # for param in expected_configured_params:
        #     assert param in calculator_params
        #     assert calculator_params[param] == \
        #            expected_configured_params[param]

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
