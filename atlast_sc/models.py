import math
from pydantic import BaseModel, root_validator
from astropy.units import Unit, Quantity
from atlast_sc.exceptions import UnitException, ValueOutOfRangeException,\
    ValueNotAllowedException, ValueTooHighException, ValueTooLowException
from atlast_sc.data import param_data_type_dicts
from atlast_sc.data import IntegrationTime, Sensitivity, Bandwidth, \
    ObsFrequency, NPol, Weather, Elevation, G, SurfaceRMS, DishRadius, TAmb, \
    EtaEff, EtaIll, EtaSpill, EtaBlock, EtaPol, EtaR, EtaQ, TCmb


class Validator:
    """
    Class providing custom validation functions
    """

    @staticmethod
    def validate_field(key, val):

        data_type = param_data_type_dicts[key]

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
                val.to(Unit(data_type['DEFAULT_UNIT'])).value
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
        if 'UNITS' not in data_type:
            return

        if unit not in data_type['UNITS']:
            raise UnitException(param, data_type['UNITS'])

    @staticmethod
    def validate_in_range(value, param, data_type):

        # Don't need to check the value is in the permitted range if
        #   there is no range specified
        if 'LOWER_VALUE' not in data_type:
            return

        # Check there's also an UPPER_VALUE
        assert 'UPPER_VALUE' in data_type

        # Get the default unit, if there is one
        unit = None if 'DEFAULT_UNIT' \
                       not in data_type else data_type['DEFAULT_UNIT']

        # If the lower value is a floor value, make sure the provided value
        # is greater than
        if 'LOWER_VALUE_IS_FLOOR' in data_type \
                and data_type['LOWER_VALUE_IS_FLOOR']:
            if value <= data_type['LOWER_VALUE']:
                raise ValueTooLowException(param, data_type['LOWER_VALUE'],
                                           unit)

        # If the upper value is a ceiling value, make sure the provided value
        # is less than
        if 'UPPER_VALUE_IS_CEIL' in data_type and \
                data_type['UPPER_VALUE_IS_CEIL']:
            if value >= data_type['UPPER_VALUE']:
                raise ValueTooHighException(param, data_type['UPPER_VALUE'],
                                            unit)

        # Do a special check for infinity (unlikely scenario, but not
        # impossible...)
        if math.isinf(value):
            raise ValueTooHighException(param, data_type['UPPER_VALUE'],
                                        unit)

        if not (data_type['LOWER_VALUE'] <=
                value <=
                data_type['UPPER_VALUE']):
            raise ValueOutOfRangeException(param,
                                           data_type['LOWER_VALUE'],
                                           data_type['UPPER_VALUE'],
                                           unit)

    @staticmethod
    def validate_allowed_values(value, param, data_type):

        # Get the default unit, if there is one
        unit = None if 'DEFAULT_UNIT' \
                       not in data_type else data_type['DEFAULT_UNIT']

        # Don't need to check the value is allowed if there are no
        # allowed values specified
        if 'ALLOWED_VALUES' not in data_type:
            return

        if value not in data_type['ALLOWED_VALUES']:
            raise ValueNotAllowedException(param,
                                           data_type['ALLOWED_VALUES'],
                                           unit)


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
        ValueWithUnits(value=IntegrationTime.DEFAULT_VALUE.value,
                       unit=IntegrationTime.DEFAULT_UNIT.value)
    sensitivity: ValueWithUnits = \
        ValueWithUnits(value=Sensitivity.DEFAULT_VALUE.value,
                       unit=Sensitivity.DEFAULT_UNIT.value)
    bandwidth: ValueWithUnits = \
        ValueWithUnits(value=Bandwidth.DEFAULT_VALUE.value,
                       unit=Bandwidth.DEFAULT_UNIT.value)
    obs_freq: ValueWithUnits = \
        ValueWithUnits(value=ObsFrequency.DEFAULT_VALUE.value,
                       unit=ObsFrequency.DEFAULT_UNIT.value)
    n_pol: ValueWithoutUnits = \
        ValueWithoutUnits(value=NPol.DEFAULT_VALUE.value)
    weather: ValueWithoutUnits = \
        ValueWithoutUnits(value=Weather.DEFAULT_VALUE.value)
    elevation: ValueWithUnits = \
        ValueWithUnits(value=Elevation.DEFAULT_VALUE.value,
                       unit=Elevation.DEFAULT_UNIT.value)

    @root_validator
    @classmethod
    def validate_t_int_or_sens_initialised(cls, field_values):
        # Validate that at least one of 't_int' and 'sensitivity'
        # has been initialised
        if field_values["t_int"].value == 0 and \
                field_values["sensitivity"].value == 0:
            raise ValueError("Please add either a sensitivity or an "
                             "integration time to your input.")
        return field_values


class InstrumentSetup(BaseModel):
    g: ValueWithoutUnits = ValueWithoutUnits(value=G.DEFAULT_VALUE.value)
    surface_rms: ValueWithUnits = \
        ValueWithUnits(value=SurfaceRMS.DEFAULT_VALUE.value,
                       unit=SurfaceRMS.DEFAULT_UNIT.value)
    dish_radius: ValueWithUnits = \
        ValueWithUnits(value=DishRadius.DEFAULT_VALUE.value,
                       unit=DishRadius.DEFAULT_UNIT.value)
    T_amb: ValueWithUnits = \
        ValueWithUnits(value=TAmb.DEFAULT_VALUE.value,
                       unit=TAmb.DEFAULT_UNIT.value)
    eta_eff: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaEff.DEFAULT_VALUE.value)
    eta_ill: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaIll.DEFAULT_VALUE.value)
    eta_q: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaQ.DEFAULT_VALUE.value)
    eta_spill: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaSpill.DEFAULT_VALUE.value)
    eta_block: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaBlock.DEFAULT_VALUE.value)
    eta_pol: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaPol.DEFAULT_VALUE.value)
    eta_r: ValueWithoutUnits = \
        ValueWithoutUnits(value=EtaR.DEFAULT_VALUE.value)


class CalculationInput(BaseModel):
    """
    Input parameters used for the sensitivity calculation
    """

    user_input: UserInput = UserInput()
    instrument_setup: InstrumentSetup = InstrumentSetup()
    T_cmb: ValueWithUnits = \
        ValueWithUnits(value=TCmb.DEFAULT_VALUE.value,
                       unit=TCmb.DEFAULT_UNIT.value)

    @root_validator
    @classmethod
    def validate_fields(cls, field_values):
        # Flatten the field values for convenience
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
    # Dish area
    area: Quantity

    class Config:
        arbitrary_types_allowed = True

    # TODO add validator for Quantity
