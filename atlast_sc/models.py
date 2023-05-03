import math
from pydantic import BaseModel, root_validator
from astropy.units import Unit, Quantity
from atlast_sc.exceptions import UnitException, ValueOutOfRangeException,\
    ValueNotAllowedException, ValueTooHighException, ValueTooLowException
import atlast_sc.data as data


class Validator:
    """
    Class providing custom validation functions
    """

    @staticmethod
    def validate_field(key, val):

        data_type = data.param_data_type_dicts[key]

        # Validate units on Quantities
        if isinstance(val, Quantity):
            try:
                Validator.validate_units(val.unit, key, data_type)
            except UnitException as e:
                raise e

        # Validate value is allowed
        if isinstance(val, Quantity):
            # Convert the value to the default units and extract the value
            # to be validated
            value_to_validate = \
                val.to(Unit(data_type.default_unit)).value
        else:
            value_to_validate = val

        try:
            Validator.validate_allowed_values(value_to_validate,
                                              key, data_type)
        except ValueNotAllowedException as e:
            raise e

        # Validate value is in permitted range
        try:
            Validator.validate_in_range(value_to_validate,
                                        key, data_type)
        except ValueOutOfRangeException as e:
            raise e

    @staticmethod
    def validate_units(unit, param, data_type):

        # Don't need to check the units if the data type is unit-less
        if data_type.units is None:
            return

        if unit not in data_type.units:
            raise UnitException(param, data_type.units)

    @staticmethod
    def validate_in_range(value, param, data_type):

        # Don't need to check the value is in the permitted range if
        #   there is no range specified
        if data_type.lower_value is None:
            return

        # Check there's also an upper value
        assert data_type.upper_value is not None

        # If the lower value is a floor value, make sure the provided value
        # is greater than
        if data_type.lower_value_is_floor:
            if value <= data_type.lower_value:
                raise ValueTooLowException(param, data_type.lower_value,
                                           data_type.default_unit)

        # If the upper value is a ceiling value, make sure the provided value
        # is less than
        if data_type.upper_value_is_ceil:
            if value >= data_type.upper_value:
                raise ValueTooHighException(param, data_type.upper_value,
                                            data_type.default_unit)

        # Do a special check for infinity (unlikely scenario, but not
        # impossible...)
        if math.isinf(value):
            raise ValueTooHighException(param, data_type.upper_value,
                                        data_type.default_unit)

        if not (data_type.lower_value <= value <= data_type.upper_value):
            raise ValueOutOfRangeException(param,
                                           data_type.lower_value,
                                           data_type.upper_value,
                                           data_type.default_unit)

    @staticmethod
    def validate_allowed_values(value, param, data_type):

        # Don't need to check the value is allowed if there are no
        # allowed values specified
        if data_type.allowed_values is None:
            return

        if value not in data_type.allowed_values:
            raise ValueNotAllowedException(param,
                                           data_type.allowed_values,
                                           data_type.default_unit)


def model_str_rep(model):
    string_rep = ""
    decimal_places = 6

    for key in model.__dict__:
        param = model.__dict__[key]

        if type(param) == ValueWithUnits or type(param) == ValueWithoutUnits:
            value = param.value
        else:
            value = param

        formatted_value = format(value, f'.{decimal_places}g')
        string_rep = string_rep + f'{key}: {formatted_value}\n'
    return string_rep


class ValueWithUnits(BaseModel):
    value: float
    unit: str

    @root_validator
    @classmethod
    def validate_fields(cls, field_values):
        """
        Validate the unit and convert the value to an astropy Quantity object
        """

        # Ensure the unit string can be converted to a valid astropy Unit
        try:
            Unit(field_values["unit"])
        except ValueError as e:
            raise ValueError(e)

        # Convert the value to an astropy Quantity object to simplify
        #   access
        field_values["value"] = \
            field_values["value"] * Unit(field_values["unit"])

        return field_values

    class Config:
        arbitrary_types_allowed = True


class ValueWithoutUnits(BaseModel):
    value: float


class UserInput(BaseModel):
    """
    Definition of the default input to the sensitivity calculation.
    The user is expected to provide some or all of this input during normal
    usage. Default values are provided for convenience.
    """

    t_int: ValueWithUnits = \
        ValueWithUnits(value=data.integration_time.default_value,
                       unit=data.integration_time.default_unit)
    sensitivity: ValueWithUnits = \
        ValueWithUnits(value=data.sensitivity.default_value,
                       unit=data.sensitivity.default_unit)
    bandwidth: ValueWithUnits = \
        ValueWithUnits(value=data.bandwidth.default_value,
                       unit=data.bandwidth.default_unit)
    obs_freq: ValueWithUnits = \
        ValueWithUnits(value=data.obs_frequency.default_value,
                       unit=data.obs_frequency.default_unit)
    n_pol: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.n_pol.default_value)
    weather: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.weather.default_value)
    elevation: ValueWithUnits = \
        ValueWithUnits(value=data.elevation.default_value,
                       unit=data.elevation.default_unit)

    @root_validator
    @classmethod
    def validate_t_int_or_sens_initialised(cls, field_values):
        """
        Validate that at least one of 't_int' and 'sensitivity'
        has been initialised
        """
        if field_values["t_int"].value == 0 and \
                field_values["sensitivity"].value == 0:
            raise ValueError("Please add either a sensitivity or an "
                             "integration time to your input.")
        return field_values

    def __str__(self):
        return model_str_rep(self)


class InstrumentSetup(BaseModel):
    g: ValueWithoutUnits = ValueWithoutUnits(value=data.g.default_value)
    surface_rms: ValueWithUnits = \
        ValueWithUnits(value=data.surface_rms.default_value,
                       unit=data.surface_rms.default_unit)
    dish_radius: ValueWithUnits = \
        ValueWithUnits(value=data.dish_radius.default_value,
                       unit=data.dish_radius.default_unit)
    T_amb: ValueWithUnits = \
        ValueWithUnits(value=data.t_amb.default_value,
                       unit=data.t_amb.default_unit)
    eta_eff: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.eta_eff.default_value)
    eta_ill: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.eta_ill.default_value)
    eta_spill: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.eta_spill.default_value)
    eta_block: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.eta_block.default_value)
    eta_pol: ValueWithoutUnits = \
        ValueWithoutUnits(value=data.eta_pol.default_value)

    def __str__(self):
        return model_str_rep(self)


class CalculationInput(BaseModel):
    """
    Input parameters used for the sensitivity calculation
    """

    user_input: UserInput = UserInput()
    instrument_setup: InstrumentSetup = InstrumentSetup()
    T_cmb: ValueWithUnits = \
        ValueWithUnits(value=data.t_cmb.default_value,
                       unit=data.t_cmb.default_unit)

    @root_validator
    @classmethod
    def validate_fields(cls, field_values):
        """
        Flatten the field values for convenience
        """
        user_input = field_values['user_input']
        instrument_setup = field_values['instrument_setup']

        flattened_field_values = {}
        for elem in user_input:
            flattened_field_values[elem[0]] = elem[1].value
        for elem in instrument_setup:
            flattened_field_values[elem[0]] = elem[1].value
        flattened_field_values['T_cmb'] = field_values['T_cmb'].value

        # Validate units and values on each field
        for key, val in flattened_field_values.items():
            try:
                Validator.validate_field(key, val)
            except ValueOutOfRangeException as e:
                raise e

        return field_values

    def validate_update(self, value_to_update, new_value):
        """
        Custom validator called manually (i.e., not as part of the Pydantic
        framework), e.g., when one of the user input values is updated.
        """

        try:
            Validator.validate_field(value_to_update, new_value)
        except ValueError as e:
            raise e

        return self


class DerivedParams(BaseModel):
    """
    Derived parameters, calculated from user input and instrument setup
    parameters.
    """

    # Atmospheric opacity
    tau_atm: float
    # Atmospheric temperature
    T_atm: Quantity
    # Receiver temperature
    T_rx: Quantity
    # Dish efficiency
    eta_a: float
    # System efficiency
    eta_s: float
    # System temperature
    T_sys: Quantity
    # Source equivalent flux density
    sefd: Quantity

    class Config:
        arbitrary_types_allowed = True

    def __str__(self):
        return model_str_rep(self)
