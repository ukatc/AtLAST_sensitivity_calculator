from contextlib import contextmanager
import pytest
from pydantic import ValidationError
from astropy.units import Unit
from atlast_sc.calculator import Calculator
from atlast_sc.exceptions import ValueTooHighException, ValueTooLowException, \
    ValueOutOfRangeException, ValueNotAllowedException, UnitException


@contextmanager
def does_not_raise():
    # Utility for checking that an exception is NOT raised
    yield


class TestCalculatorUsage:

    def test_calculator_with_defaults(self):
        # Initialise a new calculator without passing any params

        # calculator = Calculator()
        # print(calculator.calculation_parameters_as_dict)

        assert True

    def test_calculator_from_file(self):
        pass


class TestDataValidation:

    unit_exception = 'unitexception'
    value_out_of_range_exception = 'valueoutofrangeexception'
    value_too_high_exception = 'valuetoohighexception'
    value_too_low_exception = 'valuetoolowexception'
    value_not_allowed_exception = 'valuenotallowedexception'

    validation_input_data = [
        ({'t_int': {'value': 1, 'unit': 's'}}, does_not_raise(), None),
        ({'t_int': {'value': 1, 'unit': 'min'}}, does_not_raise(), None),
        ({'t_int': {'value': 0.5, 'unit': 'min'}}, does_not_raise(), None),
        ({'t_int': {'value': 1, 'unit': 'h'}}, does_not_raise(), None),
        ({'t_int': {'value': 0, 'unit': 's'}}, pytest.raises(ValidationError),
         value_too_low_exception),
        ({'t_int': {'value': float('inf'), 'unit': 's'}},
         pytest.raises(ValidationError), value_too_high_exception),
        ({'t_int': {'value': 1, 'unit': 'GHz'}},
         pytest.raises(ValidationError), unit_exception),
        ({'sensitivity': {'value': 1, 'unit': 'uJy'}}, does_not_raise(), None),
        ({'sensitivity': {'value': 1, 'unit': 'mJy'}}, does_not_raise(), None),
        ({'sensitivity': {'value': 1, 'unit': 'Jy'}}, does_not_raise(), None),
        ({'sensitivity': {'value': 0, 'unit': 'uJy'}},
         pytest.raises(ValidationError), value_too_low_exception),
        ({'sensitivity': {'value': float('inf'), 'unit': 'uJy'}},
         pytest.raises(ValidationError), value_too_high_exception),
        ({'sensitivity': {'value': 1, 'unit': 's'}},
         pytest.raises(ValidationError), unit_exception),
        ({'bandwidth': {'value': 200, 'unit': 'Hz'}}, does_not_raise(), None),
        ({'bandwidth': {'value': 200, 'unit': 'kHz'}}, does_not_raise(), None),
        ({'bandwidth': {'value': 200, 'unit': 'MHz'}}, does_not_raise(), None),
        ({'bandwidth': {'value': 200, 'unit': 'GHz'}}, does_not_raise(), None),
        ({'bandwidth': {'value': 200, 'unit': 'h'}},
         pytest.raises(ValidationError), unit_exception),
        ({'bandwidth': {'value': 0, 'unit': 'Hz'}},
         pytest.raises(ValidationError), value_too_low_exception),
        ({'bandwidth': {'value': float('inf'), 'unit': 'Hz'}},
         pytest.raises(ValidationError), value_too_high_exception),
        ({'obs_freq': {'value': 200, 'unit': 'GHz'}}, does_not_raise(), None),
        ({'obs_freq': {'value': 35, 'unit': 'GHz'}}, does_not_raise(), None),
        ({'obs_freq': {'value': 950, 'unit': 'GHz'}}, does_not_raise(), None),
        ({'obs_freq': {'value': 200, 'unit': 'Hz'}},
         pytest.raises(ValidationError), unit_exception),
        ({'obs_freq': {'value': 30, 'unit': 'GHz'}},
         pytest.raises(ValidationError), value_out_of_range_exception),
        ({'obs_freq': {'value': 960, 'unit': 'GHz'}},
         pytest.raises(ValidationError), value_out_of_range_exception),
        ({'n_pol': {'value': 1}}, does_not_raise(), None),
        ({'n_pol': {'value': 2}}, does_not_raise(), None),
        ({'n_pol': {'value': 0.5}}, pytest.raises(ValidationError),
         value_not_allowed_exception),
        ({'n_pol': {'value': 3}}, pytest.raises(ValidationError),
         value_not_allowed_exception),
        ({'weather': {'value': 50}}, does_not_raise(), None),
        ({'weather': {'value': 5}}, does_not_raise(), None),
        ({'weather': {'value': 25}}, does_not_raise(), None),
        ({'weather': {'value': 2}},
         pytest.raises(ValidationError), value_out_of_range_exception),
        ({'weather': {'value': 100}},
         pytest.raises(ValidationError), value_out_of_range_exception),
        ({'elevation': {'value': 40, 'unit': 'deg'}}, does_not_raise(), None),
        ({'elevation': {'value': 25, 'unit': 'deg'}}, does_not_raise(), None),
        ({'elevation': {'value': 85, 'unit': 'deg'}}, does_not_raise(), None),
        ({'elevation': {'value': 40, 'unit': 'Hz'}},
         pytest.raises(ValidationError), unit_exception),
        ({'elevation': {'value': 15, 'unit': 'deg'}},
         pytest.raises(ValidationError), value_out_of_range_exception),
        ({'elevation': {'value': 90, 'unit': 'deg'}},
         pytest.raises(ValidationError), value_out_of_range_exception),
    ]

    @pytest.mark.parametrize('input_data,expect_raises,exception_name',
                             validation_input_data)
    def test_data_validation_on_init(self, input_data, expect_raises,
                                     exception_name):
        # Ensure that parameters can only be initialised with data within the
        # permitted range (inclusive or exclusive), or with one of the
        # permitted values, and with incorrect units where applicable

        with expect_raises as e:
            Calculator(input_data)

        if exception_name:
            # TODO: the details of the custom exception are buried somewhere
            #  in the guts of the pydantic ValidationError, so this check (and
            #   others like it) are a bit of a clunky hack. Would be nice to
            #   find a more elegant solution
            assert exception_name in str(e.value)

    validation_input_data_for_update = [
        ({'t_int': {'value': 1, 'unit': 's'}}, does_not_raise()),
        ({'t_int': {'value': 1, 'unit': 'min'}}, does_not_raise()),
        ({'t_int': {'value': 0.5, 'unit': 'min'}}, does_not_raise()),
        ({'t_int': {'value': 1, 'unit': 'h'}}, does_not_raise()),
        ({'t_int': {'value': 0, 'unit': 's'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'t_int': {'value': float('inf'), 'unit': 's'}},
         pytest.raises(ValueTooHighException)),
        ({'t_int': {'value': 1, 'unit': 'GHz'}},
         pytest.raises(UnitException)),
        ({'sensitivity': {'value': 1, 'unit': 'uJy'}}, does_not_raise()),
        ({'sensitivity': {'value': 1, 'unit': 'mJy'}}, does_not_raise()),
        ({'sensitivity': {'value': 1, 'unit': 'Jy'}}, does_not_raise()),
        ({'sensitivity': {'value': 0, 'unit': 'uJy'}},
         pytest.raises(ValueTooLowException)),
        ({'sensitivity': {'value': float('inf'), 'unit': 'uJy'}},
         pytest.raises(ValueTooHighException)),
        ({'sensitivity': {'value': 1, 'unit': 's'}},
         pytest.raises(UnitException)),
        ({'bandwidth': {'value': 200, 'unit': 'Hz'}}, does_not_raise()),
        ({'bandwidth': {'value': 200, 'unit': 'kHz'}}, does_not_raise()),
        ({'bandwidth': {'value': 200, 'unit': 'MHz'}}, does_not_raise()),
        ({'bandwidth': {'value': 200, 'unit': 'GHz'}}, does_not_raise()),
        ({'bandwidth': {'value': 200, 'unit': 'h'}},
         pytest.raises(UnitException)),
        ({'bandwidth': {'value': 0, 'unit': 'Hz'}},
         pytest.raises(ValueTooLowException)),
        ({'bandwidth': {'value': float('inf'), 'unit': 'Hz'}},
         pytest.raises(ValueTooHighException)),
        ({'obs_freq': {'value': 200, 'unit': 'GHz'}}, does_not_raise()),
        ({'obs_freq': {'value': 35, 'unit': 'GHz'}}, does_not_raise()),
        ({'obs_freq': {'value': 950, 'unit': 'GHz'}}, does_not_raise()),
        ({'obs_freq': {'value': 200, 'unit': 'Hz'}},
         pytest.raises(UnitException)),
        ({'obs_freq': {'value': 30, 'unit': 'GHz'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'obs_freq': {'value': 960, 'unit': 'GHz'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'n_pol': {'value': 1}}, does_not_raise()),
        ({'n_pol': {'value': 2}}, does_not_raise()),
        ({'n_pol': {'value': 0.5}}, pytest.raises(ValueNotAllowedException)),
        ({'n_pol': {'value': 3}}, pytest.raises(ValueNotAllowedException)),
        ({'weather': {'value': 50}}, does_not_raise()),
        ({'weather': {'value': 5}}, does_not_raise()),
        ({'weather': {'value': 25}}, does_not_raise()),
        ({'weather': {'value': 2}},
         pytest.raises(ValueOutOfRangeException)),
        ({'weather': {'value': 100}},
         pytest.raises(ValueOutOfRangeException)),
        ({'elevation': {'value': 40, 'unit': 'deg'}}, does_not_raise()),
        ({'elevation': {'value': 25, 'unit': 'deg'}}, does_not_raise()),
        ({'elevation': {'value': 85, 'unit': 'deg'}}, does_not_raise()),
        ({'elevation': {'value': 40, 'unit': 'Hz'}},
         pytest.raises(UnitException)),
        ({'elevation': {'value': 15, 'unit': 'deg'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'elevation': {'value': 90, 'unit': 'deg'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'dish_radius': {'value': 30, 'unit': 'm'}}, does_not_raise()),
        ({'dish_radius': {'value': 1, 'unit': 'm'}}, does_not_raise()),
        ({'dish_radius': {'value': 50, 'unit': 'm'}}, does_not_raise()),
        ({'dish_radius': {'value': 0.5, 'unit': 'm'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'dish_radius': {'value': 110, 'unit': 'm'}},
         pytest.raises(ValueOutOfRangeException)),
        ({'dish_radius': {'value': 20, 'unit': 'km'}},
         pytest.raises(UnitException)),
    ]

    @pytest.mark.parametrize('input_data,expect_raises',
                             validation_input_data_for_update)
    def test_data_validation_on_update(self, input_data, expect_raises):

        # Initialise the calculator with default values
        calculator = Calculator()

        with expect_raises:
            for key, val in input_data.items():
                if 'unit' in val:
                    value = val['value'] * Unit(val["unit"])
                else:
                    value = val['value']

                setattr(calculator, key, value)

    input_data_check_derived_params = [
        ({'t_int': {'value': 1, 'unit': 's'}}, False),
        ({'sensitivity': {'value': 1, 'unit': 'uJy'}}, False),
        ({'bandwidth': {'value': 200, 'unit': 'GHz'}}, True),
        ({'bandwidth': {'value': 100, 'unit': 'MHz'}}, False),
        ({'bandwidth': {'value': 200, 'unit': 'h'}}, False),
        ({'obs_freq': {'value': 200, 'unit': 'GHz'}}, True),
        ({'obs_freq': {'value': 100, 'unit': 'GHz'}}, False),
        ({'obs_freq': {'value': 200, 'unit': 'Hz'}}, False),
        ({'n_pol': {'value': 1}}, True),
        ({'n_pol': {'value': 2}}, False),
        ({'n_pol': {'value': 0.5}}, False),
        ({'weather': {'value': 50}}, True),
        ({'weather': {'value': 25}}, False),
        ({'weather': {'value': 2}}, False),
        ({'elevation': {'value': 40, 'unit': 'deg'}}, True),
        ({'elevation': {'value': 45, 'unit': 'deg'}}, False),
        ({'elevation': {'value': 40, 'unit': 'Hz'}}, False),
        ({'dish_radius': {'value': 30, 'unit': 'm'}}, True),
        ({'dish_radius': {'value': 25, 'unit': 'm'}}, False),
        ({'dish_radius': {'value': 0.5, 'unit': 'm'}}, False),
    ]

    @pytest.mark.parametrize('input_data,expect_derived_params_recalculated',
                             input_data_check_derived_params)
    def tests_derived_params_recalculated(self, input_data,
                                          expect_derived_params_recalculated,
                                          mocker):
        # Check that the derived parameters are recalculated when parameters
        # are successfully updated, unless the updated parameter is t_int
        # or sensitivity

        # Initialise the calculator with default values
        calculator = Calculator()

        # Ensure that the appropriate validation takes place when parameters
        # are updated directly
        derived_params_spy = \
            mocker.spy(Calculator,
                       '_calculate_derived_parameters')

        for key, val in input_data.items():
            if 'unit' in val:
                value = val['value'] * Unit(val["unit"])
            else:
                value = val['value']

            try:
                setattr(calculator, key, value)
            except ValueError:
                # Do nothing. We're not interested in the specifics of the
                # update error
                pass

            # Verify that the derived parameters were recalculated
            # (unless the updated parameter is 't_int' or 'sensitivity'
            if expect_derived_params_recalculated:
                derived_params_spy.assert_called_once()
            else:
                derived_params_spy.assert_not_called()

    def test_value_is_float(self):
        pass
