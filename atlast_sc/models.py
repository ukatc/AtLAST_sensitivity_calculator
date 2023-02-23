from pydantic import BaseModel, root_validator
from astropy.units import Unit, Quantity
from atlast_sc.exceptions import UnitException, ValueOutOfRangeException,\
    ValueNotAllowedException
from atlast_sc.data import param_data_type_dicts
from atlast_sc.data import IntegrationTime, Sensitivity, Bandwidth, \
    ObsFrequency, NPol, Weather, Elevation


################################
# Custom validation functions  #
################################

def validate_units(unit, param, data_type):

    # Don't need to check the units if the data type is unit-less
    if not hasattr(data_type, 'UNITS'):
        return

    print('here and about to validate units...')
    if unit not in data_type.UNITS:
        raise UnitException(param, data_type.UNITS)


def validate_in_range(value, param, data_type):

    # Don't need to check the value is in the permitted range if
    #   there is no range specified
    if not hasattr(data_type, 'LOWER_VALUE'):
        return

    # Check there's also an UPPER_VALUE
    assert hasattr(data_type, 'UPPER_VALUE')

    if not (data_type.LOWER_VALUE <=
            value <=
            data_type.UPPER_VALUE):
        raise ValueOutOfRangeException(param,
                                       data_type.LOWER_VALUE,
                                       data_type.UPPER_VALUE,
                                       data_type.UNITS)


def validate_allowed_values(value, param, data_type):

    # Don't need to check the value is allowed if there are no
    # allowed values specified
    if not hasattr(data_type, 'ALLOWED_VALUES'):
        return

    if value not in data_type.ALLOWED_VALUES:
        raise ValueNotAllowedException(param,
                                       data_type.ALLOWED_VALUES,
                                       data_type.UNITS)


class ValueWithUnits(BaseModel):
    value: float
    unit: str
    quantity: Quantity = None

    @root_validator()
    @classmethod
    def validate_fields(cls, field_values):
        # TODO: this validation is happening twice for user input. Once for
        #  the defaults, and then again for the user-supplied values.
        #  Can we prevent validation of defaults?
        """
        Validate the unit and convert the value to an astropy Quantity object
        """
        print('validating field values', field_values)
        # Ensure the unit string can be converted to a valid astropy Unit
        try:
            Unit(field_values["unit"])
        except ValueError as e:
            raise ValueError(e)

        # Convert the value to an astropy Quantity object
        field_values["quantity"] = \
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

    @root_validator()
    @classmethod
    def validate_fields(cls, field_values):

        # Validate that at least one of 't_int' and 'sensitivity'
        # has been initialised
        if field_values["t_int"].value == 0 and \
                field_values["sensitivity"].value == 0:
            raise ValueError("Please add either a sensitivity or an "
                             "integration time to your input.")

        print('field values:', field_values)

        # Validate units and values
        for key, val in field_values.items():
            # TODO: Figure out what's going on here. The try-except is required
            #   because this validation is happening twice, and the second
            #   time round, field_values contains fields from the
            #   InstrumentSetup model. Need to understand why the validation
            #   is happening more than once, and also why it contains these
            #   unexpected parameters
            try:
                # Get the dictionary representation of the data type
                # corresponding to the current field being validated
                data_type_dict = param_data_type_dicts[key]
            except KeyError:
                continue

            # Validate units on values with units
            if isinstance(val, ValueWithUnits):
                try:
                    validate_units(val.unit, key, data_type_dict)
                except UnitException as e:
                    raise e

            # Validate value ia allowed
            try:
                validate_allowed_values(val.value, key, data_type_dict)
            except ValueNotAllowedException as e:
                raise e

            # Validate value is in permitted range
            try:
                validate_in_range(val.value, key, data_type_dict)
            except ValueOutOfRangeException as e:
                raise e

        return field_values


class InstrumentSetup(BaseModel):
    g: ValueWithoutUnits = ValueWithoutUnits(value=1)
    surface_rms: ValueWithUnits = ValueWithUnits(value=25, unit="micron")
    # TODO: might want to all users to modify radius
    dish_radius: ValueWithUnits = ValueWithUnits(value=25, unit="m")
    T_amb: ValueWithUnits = ValueWithUnits(value=270, unit="K")
    # TODO: might want to allow users to modify T_rx
    # TODO: T_rx should be calculated, not set (dependend of obs_freq))
    T_rx: ValueWithUnits = ValueWithUnits(value=50, unit="K")
    eta_eff: ValueWithoutUnits = ValueWithoutUnits(value=0.80)
    # TODO: Docs say that eta_ill "defaults to value 0.63") What's the correct
    #  default?
    eta_ill: ValueWithoutUnits = ValueWithoutUnits(value=0.80)
    # TODO: What is eta_q and what default value should it have?
    eta_q: ValueWithoutUnits = ValueWithoutUnits(value=0.96)
    eta_spill: ValueWithoutUnits = ValueWithoutUnits(value=0.95)
    eta_block: ValueWithoutUnits = ValueWithoutUnits(value=0.94)
    eta_pol: ValueWithoutUnits = ValueWithoutUnits(value=0.99)
    eta_r: ValueWithoutUnits = ValueWithoutUnits(value=1)


class CalculationInput(UserInput, InstrumentSetup):
    """
    Input parameters used for the sensitivity calculation
    """

    user_input: UserInput = UserInput()
    instrument_setup: InstrumentSetup = InstrumentSetup()
    T_cmb: ValueWithUnits = ValueWithUnits(value=2.73, unit="K")

    @root_validator()
    @classmethod
    def extract_values(cls, field_values):
        """
        Simplify the structure by only returning the value or quantity as
        appropriate
        """
        simplified_field_values = {}
        for key, val in field_values.items():
            # use the quantity, if it exists
            if hasattr(val, "quantity"):
                simplified_field_values[key] = val.quantity
            # or just use the unit-less value
            elif hasattr(val, "value"):
                simplified_field_values[key] = val.value
            else:
                # do nothing with this attribute
                continue

        return simplified_field_values


class CalculatedParams(BaseModel):
    """
    Calculated parameters used for the sensitivity calculation
    """

    # Atmospheric opacity
    tau_atm: float
    # Atmospheric temperature
    T_atm: Quantity
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


class SensitivityCalculatorParameters(BaseModel):
    """
    All parameters used in the sensitivity calculation
    """

    calculation_inputs: CalculationInput
    calculated_params: CalculatedParams

    def calculator_params(self):
        """
        Flatten the structure of the object and return properties as a
        single-level dictionary
        """

        return dict((x, y) for x, y in
                    self.calculation_inputs) | dict((x, y)
                                                    for x, y
                                                    in self.calculated_params)
