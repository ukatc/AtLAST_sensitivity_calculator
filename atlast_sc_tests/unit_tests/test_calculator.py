import copy
import pytest
import astropy.units as u
from atlast_sc.factory import CalculatorFactory
from atlast_sc.calculator import Calculator
from atlast_sc.parameter_setup import ParameterSetup
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.models import DerivedParams, CalculationInput
from atlast_sc.utils import DataHelper
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc_tests.utils import does_not_raise


class TestCalculator:

    def iterate_over_properties(self, parameter_class):
        """
        Iterate over the given class and create a dictionary
        where the property names are keys and have their 
        corresponding values.
        """
        properties = {}
        for attr in dir(parameter_class):
            if not attr.startswith('__') and \
               not attr.startswith('_') and \
               attr != 'show':
                properties[attr] = getattr(parameter_class, attr)
        return properties

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
                                   telescope_and_environment_dict,
                                   mocker):

        check_input_param_names_spy \
            = mocker.spy(ParameterSetup, '_check_input_param_names')
        derived_params_spy = \
            mocker.spy(ParameterSetup,
                       '_calculate_derived_parameters')

        # Initialize the calculator
        test_calculator_factory = CalculatorFactory(user_input=input_data)
        test_calculator = test_calculator_factory.calculator

        # Make sure the param names in user input data were validated
        check_input_param_names_spy.assert_called_with(input_data)
        # Make sure the derived parameters were calculated
        derived_params_spy.assert_called_once()

        # Initialise the parameter setup object for readability
        param_setup = test_calculator._param_setup

        # Make sure calculator contains a param_setup object with
        # calculation inputs
        assert isinstance(param_setup.calculation_inputs,
                          CalculationInput)
        
        # Make sure user input object contains a derived parameters model
        assert isinstance(test_calculator._param_setup._derived_parameters_model, 
                          DerivedParams)

        # Check that the calculator has been configured with the correct
        # input data
        for user_input_param in user_input_dict:
            if user_input_param not in expected_custom_values:
                assert getattr(test_calculator.user_input, user_input_param) \
                       == user_input_dict[user_input_param]
            else:
                assert getattr(test_calculator.user_input, user_input_param) \
                       == expected_custom_values[user_input_param]

        # Check that parameter setup has been configured with the correct
        # telescope and environment data
        for tel_and_env_param in telescope_and_environment_dict:
            assert getattr(param_setup.telescope_and_environment, tel_and_env_param).value \
                == telescope_and_environment_dict[tel_and_env_param]

        # Check that all the calculator properties are correctly mapped
        # User inputs
        user_input_params = self.iterate_over_properties(test_calculator.user_input)
        for param, value in user_input_params.items():
            if param == 'derived_parameters':
                continue # ignoring derived parameters as it is checked later
            assert value == getattr(param_setup.calculation_inputs.user_input, param).value

        # Telescope and environment
        tcope_and_env_params = self.iterate_over_properties(test_calculator.telescope_and_environment)
        for param, value in tcope_and_env_params.items():
            assert value == getattr(param_setup.calculation_inputs.telescope_and_environment,
                                    param).value
        # Derived parameters
        derived_params = self.iterate_over_properties(test_calculator.derived_parameters)
        for param, value in derived_params.items():
            assert value == getattr(test_calculator.derived_parameters, param)

    @pytest.mark.parametrize(
        'user_input,expected_raises',
        [
            ({'tint': {'value': 1, 'unit': 's'}}, pytest.raises(ValueError)),
            ({'t_int': {'val': 1, 'unit': 's'}}, pytest.raises(KeyError))
        ]
    )
    def test_initialize_calculator_invalid(self, user_input, expected_raises):
        with expected_raises:
            CalculatorFactory(user_input=user_input)
    # TO DO: Add unit tests for the case where finetune=True
    @pytest.mark.parametrize(
        'param,new_value,derived_params_recalculated,expected_raises,finetuned',
        [
            # User input
            ('t_int', 1 * u.s, False, does_not_raise(),False),
            ('sensitivity', 3 * u.mJy, False, does_not_raise(),False),
            # ('bandwidth', 10 * u.MHz, False, does_not_raise(),False),
            ('bandwidth', 10 * u.MHz, True, does_not_raise(),True),
            ('n_pol', 1, False, does_not_raise(),False),
            ('weather', 35, True, does_not_raise(),False),
            ('elevation', 80 * u.deg, True, does_not_raise(),False),
            ('obs_freq', 700 * u.GHz, True, does_not_raise(),False)
        ]
    )
    def test_update_properties_user_input(self, param, new_value,
                               derived_params_recalculated, expected_raises, finetuned,
                               t_atm, calculator, mocker, request):

        validation_spy = mocker.spy(DataHelper, 'validate')
        calculate_derived_params_spy = \
            mocker.spy(ParameterSetup, '_calculate_derived_parameters')
        original_derived_params = copy.deepcopy(calculator.derived_parameters)

        uip = calculator.user_input
        # Check that we can update certain properties, but not others
        with expected_raises as e:
            setattr(uip, param, new_value)

        if not e:
            # Verify that the update was validated
            validation_spy.assert_called()
            # Verify that the parameter was updated
            assert getattr(uip, param) == new_value
            # Verify that the derived parameters were updated,
            # where appropriate
            if derived_params_recalculated:
                if finetuned:
                    calculate_derived_params_spy.assert_called()
                    assert calculator.derived_parameters == original_derived_params                
                else:
                    calculate_derived_params_spy.assert_called()
                    assert False == calculator.derived_parameters.__eq__(original_derived_params)
                        
            else:
                calculate_derived_params_spy.assert_not_called()
                assert calculator.derived_parameters == \
                    original_derived_params
        else:
            # Verify that that parameter was not updated
            original_value = request.getfixturevalue(param.lower())
            assert getattr(uip, param) == original_value

    @pytest.mark.parametrize(
        'param,new_value,derived_params_recalculated,expected_raises,finetuned',
        [
            # Telescope and environment
            ('surface_rms', 10 * u.micron, False,
             pytest.raises(AttributeError),False),
            ('dish_radius', 30 * u.m, True, does_not_raise(),False),
            ('eta_eff', 0.7, False, pytest.raises(AttributeError),False),
            ('eta_ill', 0.7, False, pytest.raises(AttributeError),False),
            ('eta_spill', 0.7, False, pytest.raises(AttributeError),False),
            ('T_cmb', 10 * u.K, False, pytest.raises(AttributeError),False),
            ('T_amb', 100 * u.K, False, pytest.raises(AttributeError),False),
            ('eta_block', 0.7, False, pytest.raises(AttributeError),False),
            ('eta_pol', 0.7, False, pytest.raises(AttributeError),False)
        ]
    )
    def test_update_properties_telescope_and_environment(self, param, new_value,
                               derived_params_recalculated, expected_raises, finetuned,
                               t_atm, calculator, mocker, request):

        validation_spy = mocker.spy(DataHelper, 'validate')
        calculate_derived_params_spy = \
            mocker.spy(ParameterSetup, '_calculate_derived_parameters')
        original_derived_params = copy.deepcopy(calculator.derived_parameters)


        uip = calculator.user_input
        taep = calculator.telescope_and_environment
        # Check that we can update certain properties, but not others
        with expected_raises as e:
            setattr(taep, param, new_value)

        if not e:
            # Verify that the update was validated
            validation_spy.assert_called()
            # Verify that the parameter was updated
            assert getattr(taep, param) == new_value
            # Verify that the derived parameters were updated,
            # where appropriate
            if derived_params_recalculated:
                if finetuned:
                    calculate_derived_params_spy.assert_called()
                    assert calculator.derived_parameters == original_derived_params                
                else:
                    calculate_derived_params_spy.assert_called()
                    assert False == calculator.derived_parameters.__eq__(original_derived_params)
                        
            else:
                calculate_derived_params_spy.assert_not_called()
                assert calculator.derived_parameters == \
                    original_derived_params
        else:
            # Verify that that parameter was not updated
            original_value = request.getfixturevalue(param.lower())
            assert getattr(taep, param) == original_value

    @pytest.mark.parametrize(
        'param,new_value,derived_params_recalculated,expected_raises,finetuned',
        [
            # Derived parameters
            ('transmittance', 0.3, False, pytest.raises(AttributeError),False),
            ('T_atm', 200 * u.K, False, pytest.raises(AttributeError),False),
            ('T_rx', 200 * u.K, False, pytest.raises(AttributeError),False),
            ('T_sys', 200 * u.K, False, pytest.raises(AttributeError),False),
            ('eta_a', 0.7, False, pytest.raises(AttributeError),False),
            ('eta_s', 0.7, False, pytest.raises(AttributeError),False),
            ('sefd', 1e-24 * u.J / (u.m * u.m), False, pytest.raises(AttributeError),False)
        ]
    )
    def test_update_properties_derived_parameters(self, param, new_value,
                               derived_params_recalculated, expected_raises, finetuned,
                               t_atm, calculator, mocker, request):

        original_derived_params = copy.deepcopy(calculator.derived_parameters)
        dp = calculator.derived_parameters

        # Check that we can update certain properties, but not others
        with expected_raises as e:
            setattr(dp, param, new_value)

        if e:
            # Verify that that parameters were not updated
            original_value = getattr(original_derived_params, param)
            assert getattr(dp, param) == original_value
        else:
            assert False

    def test_reset(self, obs_freq, calculator, mocker):

        calculate_derived_params_spy = \
            mocker.spy(ParameterSetup, '_calculate_derived_parameters')
        parameter_setup_reset_spy = mocker.spy(ParameterSetup, 'reset')
        original_derived_params = copy.deepcopy(calculator.derived_parameters)

        # update the calculator
        calculator.user_input.obs_freq = 850 * u.GHz

        # reset the calculator
        calculator.reset()
        assert calculator.user_input.obs_freq == obs_freq
        # Verify that the derived parameters were recalculated
        calculate_derived_params_spy.assert_called()
        assert calculator.derived_parameters == original_derived_params
        # assert calculator.user_input.derived_parameters == original_derived_params
        # Verify that the reset function resets the values stored in the
        # Calculator's parameter setup object
        parameter_setup_reset_spy.assert_called()

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
                                   calculated_sensitivity, calculator):

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
                assert calculator.user_input.t_int == new_t_int
            else:
                assert calculator.user_input.t_int == t_int
        else:
            assert calculator.user_input.t_int == t_int

        if update_calculator is not False:
            assert calculator.calculated_sensitivity == sens
        else:
            assert calculator.calculated_sensitivity == calculated_sensitivity

        # Verify that the units of the calculated sensitivity are in units of 
        # flux density
        assert any(sens.unit == x for x in [u.uJy, u.mJy, u.Jy])

    @pytest.mark.parametrize(
        'new_sens,update_calculator',
        [
            (5 * u.mJy, None),
            (5 * u.mJy, True),
            (5 * u.mJy, False),
            (None, None),
            (None, True),
            (None, False)
        ]
    )
    def test_calculate_t_integration(self, new_sens, update_calculator, calculated_t_int,
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
                assert calculator.user_input.sensitivity == new_sens
            else:
                assert calculator.user_input.sensitivity == sensitivity
        else:
            assert calculator.user_input.sensitivity == sensitivity

        if update_calculator is not False:
            assert calculator.calculated_t_int == int_time
        else:
            assert calculator.calculated_t_int == calculated_t_int

        # # Verify that the units of the calculated integration time are in
        # units of time
        assert any(int_time.unit == x for x in [u.s, u.min, u.h])

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

    # NOTE: Both calculated sensitivity and calculated integration time can be any
    # value from 0 to inf, therefore, this test has no meaning. Commenting it out
    # for any future need.
    #
    # @pytest.mark.parametrize(
    #     'param,input_value,func_name',
    #     [
    #         ('calculated_t_int', 300 * u.mJy, 'calculate_t_integration'),
    #         # Not possible to get the sensitivity down to exactly zero,
    #         # and since t_int must be greater than 1s, it's not possible
    #         # to reach the upper bound either
    #     ]
    # )
    # def test_calculate_invalid_value(self, param, input_value, func_name,
    #                                  calculator):
    #     # Verify that a warning is raised if the calculated value is outside
    #     # its permitted range
    #     with pytest.warns(CalculatedValueInvalidWarning):
    #         func = getattr(calculator, func_name)
    #         calculated_value = func(input_value)

    #     # make sure the calculator was not updated with calculated value
    #     stored_value = getattr(calculator, param)
    #     assert stored_value != calculated_value

    def test_consistency(self, calculator):
        # Calculate the sensitivity
        integration_time = calculator.calculate_t_integration()
        # Use the resulting integration time to calculate the corresponding
        # sensitivity
        calculated_sensitivity = calculator.calculate_sensitivity(integration_time,
                                                       update_calculator=False)
        # Verify that the calculated sensitivity matches the original value
        # that was used to derive the integration time
        assert round(calculated_sensitivity.value, 10) == \
               round(calculator.user_input.sensitivity.value, 10)


class TestParameterSetup:

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
    def test_initialize_parameter_setup(self, input_data, expected_custom_values,
                               scenario, user_input_dict,
                               telescope_and_environment_dict):

        param_setup = ParameterSetup(user_input=input_data)

        # Check that all the config properties are correctly mapped
        assert param_setup.calculation_inputs == param_setup._calculation_inputs
        assert param_setup._original_inputs == param_setup._calculation_inputs
