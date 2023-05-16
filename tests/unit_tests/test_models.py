import math

import pytest
from astropy import units as u
from atlast_sc.models import ModelUtils
from atlast_sc.models import ValueWithUnits, ValueWithoutUnits, \
    UserInput, CalculationInput
from atlast_sc.data import Validator
from tests.utils import does_not_raise


class TestModelUtils:

    @pytest.mark.parametrize(
        'model,expected_result',
        [
            ('test_model_with_values',
             'value1: 1.0 GHz\n'
             'value2: 2.123457e+10 s\n'
             'value3: 1.0 s\n'
             'value4: 1.123457 s'),
            ('test_model_with_literals',
             'value1: 1.3\n'
             'value2: True\n'
             'value3: hello\n'
             'value4: [1, 2, 3]'),
        ]
    )
    def test_model_str_rep(self, model, expected_result, request):
        test_model = request.getfixturevalue(model)
        result = ModelUtils.model_str_rep(test_model)
        assert result == expected_result


class TestModels:

    @pytest.mark.parametrize(
        'value,unit,expect_raises,expected_error_msg',
        [
            (1 * u.GHz, 'GHz', does_not_raise(), None),
            (1, 'GHz', does_not_raise(), None),
            (1 * u.GHz, None, does_not_raise(), None),
            (1 * u.GHz, 'MHz', pytest.raises(ValueError),
             "Ambiguous definition: unit 'MHz' does not "
             "match 'GHz' from parameter 'value'"),
            (1, 'invalid', pytest.raises(ValueError),
             "'invalid' is not a valid unit"),
            (1, None, pytest.raises(ValueError),
             "'None' is not a valid unit"),
        ]
    )
    def test_create_value_with_units(self, value, unit, expect_raises,
                                     expected_error_msg):
        with expect_raises as e:
            test_value_with_units = ValueWithUnits(value=value, unit=unit)
            assert test_value_with_units.value == 1 * u.GHz
            assert test_value_with_units.unit == 'GHz'

        if expected_error_msg:
            assert expected_error_msg in str(e.value)

    @pytest.mark.parametrize(
        'value',
        [1, 1.0]
    )
    def test_create_value_without_units(self, value):
        test_value_without_units = ValueWithoutUnits(value=value)
        assert test_value_without_units.value == 1.0

    @pytest.mark.parametrize(
        't_int,sensitivity,expect_raises',
        [
            (1, 1, does_not_raise()),
            (1, 0, does_not_raise()),
            (0, 1, does_not_raise()),
            (0, 0, pytest.raises(ValueError))
        ]
    )
    def test__validate_t_int_or_sens_initialised(self, t_int, sensitivity,
                                                 expect_raises):
        with expect_raises as e:
            input_data = {'t_int': {'value': t_int, 'unit': 's'},
                          'sensitivity': {'value': sensitivity, 'unit': 'mJy'}}
            UserInput(**input_data)

        if e:
            assert 'Please add either a sensitivity or an integration time ' \
                   'to your input' in str(e.value)

    def test_user_input_to_str(self, calculator, mocker):

        model_str_rep_spy = mocker.spy(ModelUtils, 'model_str_rep')

        str(calculator.user_input)

        model_str_rep_spy.assert_called_once()

    def test_instrument_setup_to_str(self, calculator, mocker):

        model_str_rep_spy = mocker.spy(ModelUtils, 'model_str_rep')

        str(calculator.instrument_setup)

        model_str_rep_spy.assert_called_once()

    def test_derived_params_to_str(self, calculator, mocker):

        model_str_rep_spy = mocker.spy(ModelUtils, 'model_str_rep')

        str(calculator.derived_parameters)

        model_str_rep_spy.assert_called_once()

    def test_calculation_input_validated(
            self, user_input_dict, instrument_setup_dict, t_cmb, mocker):

        validate_field_spy = mocker.spy(Validator, 'validate_field')

        CalculationInput()

        expected_validation_calls = []
        # Check that the user input and instrument setup parameters were
        # validated
        for key, val in user_input_dict.items():
            expected_validation_calls.append(mocker.call(key, val))
        for key, val in instrument_setup_dict.items():
            expected_validation_calls.append(mocker.call(key, val))
        # T_cmb should also be validata
        expected_validation_calls.append(mocker.call('T_cmb', t_cmb))

        assert validate_field_spy.mock_calls == expected_validation_calls

    @pytest.mark.parametrize(
        'param,value,unit',
        [
            ('n_pol', 3, None),
            ('t_int', 0, 's'),
            ('sensitivity', 0, 'mJy'),
            ('sensitivity', math.inf, 'mJy'),
            ('t_int', 1, 'MHz')
        ]
    )
    def test_calculation_input_handle_invalid(self, param, value, unit):
        with pytest.raises(ValueError):
            user_input = {param: {'value': value, 'unit': unit}}
            CalculationInput(user_input=user_input)
