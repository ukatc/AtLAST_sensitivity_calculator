import pytest
import astropy.units as u
from atlast_sc.data import Data, Validator
from atlast_sc.exceptions import UnitException, ValueNotAllowedException, \
    ValueOutOfRangeException, ValueTooLowException, ValueTooHighException
from tests.utils import does_not_raise


class TestData:

    def test_param_data_type_dicts(self, instrument_setup_dict,
                                   user_input_dict, t_cmb):

        # Check that data type dictionary contains the user input parameters,
        # instrument setup parameters, and T_cmb
        expected_keys = \
            [param_name for param_name in
             (user_input_dict |
              instrument_setup_dict |
              {'T_cmb': t_cmb}).keys()]

        assert list(Data.param_data_type_dicts.keys()) == expected_keys

    @pytest.mark.parametrize(
        'default_value,default_unit,lower_value,lower_value_is_floor,'
        'upper_value,upper_value_is_ceil,allowed_values,units,'
        'expected_data_conversion',
        [
            (1, 's', 0, False, 10, True, None, ['s', 'min', 'h'],
             {'s': 1, 'min': 60, 'h': 3600}),
            (1, None, None, False, None, False, [1, 2, 3], None, None)
        ]
    )
    def test_create_data_type(self, default_value, default_unit, lower_value,
                              lower_value_is_floor, upper_value,
                              upper_value_is_ceil, allowed_values, units,
                              expected_data_conversion):

        data_type = Data.DataType(default_value=default_value,
                                  default_unit=default_unit,
                                  lower_value=lower_value,
                                  lower_value_is_floor=lower_value_is_floor,
                                  upper_value=upper_value,
                                  upper_value_is_ceil=upper_value_is_ceil,
                                  allowed_values=allowed_values, units=units)
        # Verify that data conversion factors have been calculated if the
        # data type has units
        if units:
            assert data_type.data_conversion == expected_data_conversion
        else:
            assert data_type.data_conversion is None

    @pytest.mark.parametrize(
        'scenario,default_value,default_unit,lower_value,lower_value_is_floor,'
        'upper_value,upper_value_is_ceil,allowed_values,units',
        [
            ('Default value not in range (low)', 1, 's', 2, False, 10, False,
             None, ['s']),
            ('Default value not in range (high)', 11, 's', 2, False, 10, False,
             None, ['s']),
            ('Default value too low', 1, 's', 1, True, 10, False, None, ['s']),
            ('Default value too high', 10, 's', 1, False, 10, True, None,
             ['s']),
            ('Default value not permitted', 1, 's', None, False, None, False,
             [2, 3], ['s']),
            ('Default unit not in allowed list', 1, 's', 1, False, 10, False,
             None, ['h', 'min']),
            ('Invalid default unit', 1, 'z', 1, False, 10, False, None,
             ['s']),
            ('Invalid unit in allowed list', 1, 's', 1, False, 10, False, None,
             ['z']),
            ('Upper value missing', 1, 's', 1, False, None, False, None,
             ['s']),
            ('Lower value missing', 1, 's', None, False, 10, True, None,
             ['s']),
            ('Allowed values *and* range defined', 1, 's', 1, False, 10, False,
             [1, 10], ['s']),
            ('Default value is infinity', float('inf'), None, None, False,
             None, False, None, None),
            ('Lower value is infinity', 1, None, float('inf'), False,
             float('inf'), True, None, None),
            ('Lower value is greater than upper value', 10, 's',
             9, False, 8, False, None, ['s'])
        ]
    )
    def test_create_invalid_data_type(self, scenario, default_value,
                                      default_unit, lower_value,
                                      lower_value_is_floor, upper_value,
                                      upper_value_is_ceil, allowed_values,
                                      units):
        with pytest.raises((AssertionError, ValueError)):
            Data.DataType(default_value=default_value,
                          default_unit=default_unit,
                          lower_value=lower_value,
                          lower_value_is_floor=lower_value_is_floor,
                          upper_value=upper_value,
                          upper_value_is_ceil=upper_value_is_ceil,
                          allowed_values=allowed_values, units=units)


class TestValidator:

    @pytest.mark.parametrize(
        'test_unit,val,expect_validates,expected_raises',
        [
            ('s', 1 * u.s, True, does_not_raise()),
            ('s', 1, False, does_not_raise()),
            ('Hz', 1 * u.Hz, True, pytest.raises(UnitException))
        ]
    )
    def test_validate_field_unit_validated(self, test_unit, val,
                                           expect_validates, expected_raises,
                                           test_data_types,
                                           mocker):

        validate_unit_spy = mocker.spy(Validator, 'validate_units')

        with expected_raises:
            Validator.validate_field('t_int', val)
            if expect_validates:
                validate_unit_spy\
                    .assert_called_with(test_unit,
                                        't_int',
                                        test_data_types['t_int'])

    @pytest.mark.parametrize(
        'test_val,expect_validates_with,param,expected_raises',
        [
            (1, 1, 'n_pol', does_not_raise()),
            (10, 10, 'n_pol', pytest.raises(ValueNotAllowedException)),
            (1 * u.s, 1, 't_int', does_not_raise()),
            (1 * u.min, 60, 'allowed_values_with_units', does_not_raise()),
        ]
    )
    def test_validate_field_value_allowed(self, test_val,
                                          expect_validates_with,
                                          param,
                                          expected_raises,
                                          test_data_types,
                                          mocker):

        validate_allowed_values_spy = mocker.spy(Validator,
                                                 'validate_allowed_values')

        with expected_raises:
            Validator.validate_field(param, test_val)
            validate_allowed_values_spy\
                .assert_called_with(expect_validates_with,
                                    param,
                                    test_data_types[param])

    @pytest.mark.parametrize(
        'test_val,expect_validates_with,expected_raises',
        [
            (1, 1, does_not_raise()),
            (1 * u.s, 1, does_not_raise()),
            (1 * u.min, 60, does_not_raise()),
            (0, 0, pytest.raises(ValueOutOfRangeException))
        ]
    )
    def test_validate_field_value_in_range(self, test_val,
                                           expect_validates_with,
                                           expected_raises,
                                           test_data_types,
                                           mocker):

        validate_in_range_spy = mocker.spy(Validator, 'validate_in_range')

        with expected_raises:
            Validator.validate_field('t_int', test_val)
            validate_in_range_spy\
                .assert_called_with(expect_validates_with, 't_int',
                                    test_data_types['t_int'])

    @pytest.mark.parametrize(
        'test_unit,param,expected_raises',
        [
            ('s', 't_int', does_not_raise()),
            ('Hz', 't_int', pytest.raises(UnitException)),
            (None, 'n_pol', does_not_raise())
        ]
    )
    def test_validate_units(self, test_unit, param, expected_raises,
                            test_data_types):

        with expected_raises:
            Validator.validate_units(test_unit, param,
                                     test_data_types[param])

    @pytest.mark.parametrize(
        'test_value,param,expected_raises',
        [
            (200, 'obs_freq', does_not_raise()),
            (20, 'obs_freq', pytest.raises(ValueOutOfRangeException)),
            (1000, 'obs_freq', pytest.raises(ValueOutOfRangeException)),
            (0, 'sensitivity', pytest.raises(ValueTooLowException)),
            (1e10, 'sensitivity', pytest.raises(ValueTooHighException)),
            (float('inf'), 't_int', pytest.raises(ValueTooHighException)),
            (1, 'n_pol', does_not_raise())
        ]
    )
    def test_validate_in_range(self, test_value, param, expected_raises,
                               test_data_types):
        with expected_raises:
            Validator.validate_in_range(test_value, param,
                                        test_data_types[param])

    @pytest.mark.parametrize(
        'test_value,param,expected_raises',
        [
            (1, 'n_pol', does_not_raise()),
            (3, 'n_pol', pytest.raises(ValueNotAllowedException)),
            (1, 't_int', does_not_raise())
        ]
    )
    def test_validate_allowed_values(self, test_value, param, expected_raises,
                                     test_data_types):
        with expected_raises:
            Validator.validate_allowed_values(test_value, param,
                                              test_data_types[param])
