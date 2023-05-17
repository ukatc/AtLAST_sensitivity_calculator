import copy
import pytest
import astropy.units as u
from atlast_sc.calculator import Calculator, Config
from atlast_sc.models import DerivedParams, CalculationInput
from atlast_sc.utils import DataHelper
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from tests.utils import does_not_raise


class TestCalculator:

    @pytest.mark.parametrize(
        'input_data,expected_custom_values,scenario',
        [
            ({}, {}, 'Default values used'),
            ({'t_int': {'value': 1, 'unit': 's'},
              'bandwidth': {'value': 10, 'unit': 'MHz'},
              'n_pol': {'value': 1}},
             {'t_int': 1 * u.s, 'bandwidth': 10 * u.MHz, 'n_pol': 1},
             'Some custom values and defaults for the rest'
             )
        ]
    )
    def test_initialize_calculator(self, input_data, expected_custom_values,
                                   scenario, user_input_dict,
                                   instrument_setup_dict, mocker):

        check_input_param_names_spy \
            = mocker.spy(Calculator, '_check_input_param_names')
        derived_params_spy = \
            mocker.spy(Calculator,
                       '_calculate_derived_parameters')

        # Initialize the calculator
        test_calculator = Calculator(input_data)

        # Make sure the param names in user input data were validated
        check_input_param_names_spy.assert_called_with(input_data)
        # Make sure the derived parameters were calculated
        derived_params_spy.assert_called_once()

        # Make sure calculator contains a config object with
        # calculation inputs, and a derived params object
        assert isinstance(test_calculator._config.calculation_inputs,
                          CalculationInput)
        assert isinstance(test_calculator._derived_params, DerivedParams)

        # Check that the calculator has been configured with the correct
        # input data
        for user_input_param in user_input_dict:
            if user_input_param not in expected_custom_values:
                assert getattr(test_calculator, user_input_param) \
                       == user_input_dict[user_input_param]
            else:
                assert getattr(test_calculator, user_input_param) \
                       == expected_custom_values[user_input_param]

        for instrument_setup_param in instrument_setup_dict:
            assert getattr(test_calculator, instrument_setup_param) \
                   == instrument_setup_dict[instrument_setup_param]

        # Check that all the calculator properties are correctly mapped
        assert test_calculator.calculation_inputs \
               == test_calculator._config.calculation_inputs
        assert test_calculator.calculation_inputs.user_input \
               == test_calculator.user_input
        assert test_calculator.calculation_inputs.user_input \
               == test_calculator._config.calculation_inputs.user_input
        assert test_calculator.calculation_inputs.instrument_setup \
               == test_calculator.instrument_setup
        assert test_calculator.calculation_inputs.instrument_setup \
               == test_calculator._config.calculation_inputs.instrument_setup

        # Make sure the derived parameters are mapped correctly
        for param in test_calculator.derived_parameters:
            assert getattr(test_calculator, param[0]) == param[1]

    @pytest.mark.parametrize(
        'user_input,expected_raises',
        [
            ({'tint': {'value': 1, 'unit': 's'}}, pytest.raises(ValueError)),
            ({'t_int': {'val': 1, 'unit': 's'}}, pytest.raises(KeyError))
        ]
    )
    def test_initialize_calculator_invalid(self, user_input, expected_raises):
        with expected_raises:
            Calculator(user_input)

    @pytest.mark.parametrize(
        'param,new_value,derived_params_recalculated,expected_raises',
        [
            # User input
            ('t_int', 1 * u.s, False, does_not_raise()),
            ('sensitivity', 3 * u.mJy, False, does_not_raise()),
            ('bandwidth', 10 * u.MHz, False, does_not_raise()),
            ('n_pol', 1, False, does_not_raise()),
            ('weather', 35, True, does_not_raise()),
            ('elevation', 80 * u.deg, True, does_not_raise()),
            ('obs_freq', 700 * u.GHz, True, does_not_raise()),
            # Instrument setup
            ('dish_radius', 30 * u.m, True, does_not_raise()),
            ('g', 0.9, False, pytest.raises(AttributeError)),
            ('surface_rms', 10 * u.micron, False,
             pytest.raises(AttributeError)),
            ('T_amb', 100 * u.K, False, pytest.raises(AttributeError)),
            ('eta_eff', 0.7, False, pytest.raises(AttributeError)),
            ('eta_ill', 0.7, False, pytest.raises(AttributeError)),
            ('eta_spill', 0.7, False, pytest.raises(AttributeError)),
            ('eta_block', 0.7, False, pytest.raises(AttributeError)),
            ('eta_pol', 0.7, False, pytest.raises(AttributeError)),
            # Derived parameters
            ('tau_atm', 0.3, False, pytest.raises(AttributeError)),
            ('T_atm', 200 * u.K, False, pytest.raises(AttributeError)),
            ('T_rx', 200 * u.K, False, pytest.raises(AttributeError)),
            ('T_sys', 200 * u.K, False, pytest.raises(AttributeError)),
            ('eta_a', 0.7, False, pytest.raises(AttributeError)),
            ('eta_s', 0.7, False, pytest.raises(AttributeError)),
            ('sefd', 1e-24 * u.J / (u.m * u.m), False,
             pytest.raises(AttributeError)),
            # Other calculation input
            ('T_cmb', 10 * u.K, False, pytest.raises(AttributeError))
        ]
    )
    def test_update_properties(self, param, new_value,
                               derived_params_recalculated, expected_raises,
                               t_atm, calculator, mocker, request):

        validation_spy = mocker.spy(DataHelper, 'validate')
        calculate_derived_params_spy = \
            mocker.spy(Calculator, '_calculate_derived_parameters')
        original_derived_params = copy.deepcopy(calculator.derived_parameters)

        # Check that we can update certain properties, but not others
        with expected_raises as e:
            setattr(calculator, param, new_value)

        if not e:
            # Verify that the update was validated
            validation_spy.assert_called()
            # Verify that the parameter was updated
            assert getattr(calculator, param) == new_value
            # Verify that the derived parameters were updated,
            # where appropriate
            if derived_params_recalculated:
                calculate_derived_params_spy.assert_called()
                assert calculator.derived_parameters != \
                       original_derived_params
            else:
                calculate_derived_params_spy.assert_not_called()
                assert calculator.derived_parameters == \
                       original_derived_params
        else:
            # Verify that that parameter was not updated
            original_value = request.getfixturevalue(param.lower())
            assert getattr(calculator, param) == original_value

    def test_reset(self, obs_freq, calculator, mocker):

        calculate_derived_params_spy = \
            mocker.spy(Calculator, '_calculate_derived_parameters')
        config_reset_spy = mocker.spy(Config, 'reset')
        original_derived_params = copy.deepcopy(calculator.derived_parameters)

        # update the calculator
        calculator.obs_freq = 850 * u.GHz

        # reset the calculator
        calculator.reset()
        assert calculator.obs_freq == obs_freq
        # Verify that the derived parameters were recalculated
        calculate_derived_params_spy.assert_called()
        assert calculator.derived_parameters == original_derived_params
        # Verify that the reset function resets the values stored in the
        # Calculator's config object
        config_reset_spy.assert_called()

    @pytest.mark.parametrize(
        'new_t_int,update_calculator',
        [
            (10 * u.s, None),
            (10 * u.s, True),
            (10 * u.s, False),
            (None, None),
            (None, True),
            (None, False)
        ]
    )
    def test_calculate_sensitivity(self, new_t_int, update_calculator, t_int,
                                   sensitivity, calculator):

        if new_t_int is not None:
            if update_calculator is not None:
                # Pass the new integration time and the update calculator
                # flag to the function
                sens = \
                    calculator.calculate_sensitivity(new_t_int,
                                                     update_calculator)
            else:
                # Pass the new integration time to the function
                sens = calculator.calculate_sensitivity(new_t_int)
        else:
            if update_calculator is not None:
                # Pass the update calculator flag to the function
                sens = \
                    calculator.calculate_sensitivity(
                        update_calculator=update_calculator
                    )
            else:
                # Call the function without arguments
                sens = calculator.calculate_sensitivity()

        # Verify that the calculator has been updated with the new integration
        # time and calculated sensitivity, where appropriate
        # (the default behaviour is to update the calculator, hence we need
        # a specific check for 'False' here)
        if new_t_int is not None:
            if update_calculator is not False:
                assert calculator.t_int == new_t_int
            else:
                assert calculator.t_int == t_int
        else:
            assert calculator.t_int == t_int

        if update_calculator is not False:
            assert calculator.sensitivity == sens
        else:
            assert calculator.sensitivity == sensitivity

        # Verify that the units of the calculated sensitivity are in mJy
        assert sens.unit == u.mJy

    @pytest.mark.parametrize(
        'new_sens,update_calculator',
        [
            (10 * u.mJy, None),
            (10 * u.mJy, True),
            (10 * u.mJy, False),
            (None, None),
            (None, True),
            (None, False)
        ]
    )
    def test_calculate_t_integration(self, new_sens, update_calculator, t_int,
                                     sensitivity, calculator):

        if new_sens is not None:
            if update_calculator is not None:
                # Pass the new sensitivity and the update calculator
                # flag to the function
                int_time = \
                    calculator.calculate_t_integration(
                        new_sens, update_calculator
                    )
            else:
                # Pass the new sensitivity time to the function
                int_time = calculator.calculate_t_integration(new_sens)
        else:
            if update_calculator is not None:
                # Pass the update calculator flag to the function
                int_time = \
                    calculator.calculate_t_integration(
                        update_calculator=update_calculator
                    )
            else:
                # Call the function without arguments
                int_time = calculator.calculate_t_integration()

        # Verify that the calculator has been updated with the new sensitivity
        # and calculated integration time, where appropriate
        # (the default behaviour is to update the calculator, hence we need
        # a specific check for 'False' here)
        if new_sens is not None:
            if update_calculator is not False:
                assert calculator.sensitivity == new_sens
            else:
                assert calculator.sensitivity == sensitivity
        else:
            assert calculator.sensitivity == sensitivity

        if update_calculator is not False:
            assert calculator.t_int == int_time
        else:
            assert calculator.t_int == t_int

        # # Verify that the units of the calculated integration time are in
        # seconds
        assert int_time.unit == u.s

    @pytest.mark.parametrize(
        'input_value,func_name',
        [
            (0.5 * u.s, 'calculate_sensitivity'),
            (0, 'calculate_t_integration')
        ]
    )
    def test_calculate_with_invalid_input(self, input_value, func_name,
                                          calculator):
        # Verify that the input value is correctly flagged as invalid
        with pytest.raises(ValueError):
            func = getattr(calculator, func_name)
            func(input_value)

    @pytest.mark.parametrize(
        'param,input_value,func_name',
        [
            ('t_int', 300 * u.mJy, 'calculate_t_integration'),
            # Not possible to get the sensitivity down to exactly zero,
            # and since t_int must be greater than 1s, it's not possible
            # to reach the upper bound either
        ]
    )
    def test_calculate_invalid_value(self, param, input_value, func_name,
                                     calculator):
        # Verify that a warning is raised if the calculated value is outside
        # its permitted range
        with pytest.warns(CalculatedValueInvalidWarning):
            func = getattr(calculator, func_name)
            calculated_value = func(input_value)

        # make sure the calculator was not updated with calculated value
        stored_value = getattr(calculator, param)
        assert stored_value != calculated_value

    def test_consistency(self, calculator):
        # Calculate the sensitivity
        integration_time = calculator.calculate_t_integration()
        # Use the resulting integration time to calculate the corresponding
        # sensitivity
        sensitivity = calculator.calculate_sensitivity(integration_time,
                                                       update_calculator=False)
        # Verify that the calculated sensitivity matches the original value
        # that was used to derive the integration time
        assert round(sensitivity.value, 10) == \
               round(calculator.sensitivity.value, 10)


class TestConfig:

    @pytest.mark.parametrize(
        'input_data,expected_custom_values,scenario',
        [
            ({}, {}, 'Default values used'),
            ({'t_int': {'value': 1, 'unit': 's'},
              'bandwidth': {'value': 10, 'unit': 'MHz'},
              'n_pol': {'value': 1}},
             {'t_int': 1 * u.s, 'bandwidth': 10 * u.MHz, 'n_pol': 1},
             'Some custom values and defaults for the rest'
             )
        ]
    )
    def test_initialize_config(self, input_data, expected_custom_values,
                               scenario, user_input_dict,
                               instrument_setup_dict):

        config = Config(input_data)

        # Check that all the config properties are correctly mapped
        assert config.calculation_inputs == config._calculation_inputs
        assert config._original_inputs == config._calculation_inputs
