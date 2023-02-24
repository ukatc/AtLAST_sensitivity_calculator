from pydantic import BaseModel, root_validator
from astropy.units import Unit, Quantity
from atlast_sc.exceptions import UnitException, ValueOutOfRangeException,\
    ValueNotAllowedException
from atlast_sc.data import param_data_type_dicts
from atlast_sc.data import IntegrationTime, Sensitivity, Bandwidth, \
    ObsFrequency, NPol, Weather, Elevation, G, SurfaceRMS, DishRadius, TAmb, \
    TRx, EtaEff, EtaIll, EtaSpill, EtaBlock, EtaPol, EtaR, EtaQ, TCmb


###################################################
# Custom validation and transformation functions  #
###################################################

def validate_units(unit, param, data_type):

    # Don't need to check the units if the data type is unit-less
    if 'UNITS' not in data_type:
        return

    if unit not in data_type['UNITS']:
        raise UnitException(param, data_type['UNITS'])


def validate_in_range(value, param, data_type):

    # Don't need to check the value is in the permitted range if
    #   there is no range specified
    if 'LOWER_VALUE' not in data_type:
        return

    # Check there's also an UPPER_VALUE
    assert 'UPPER_VALUE' in data_type

    if not (data_type['LOWER_VALUE'] <=
            value <=
            data_type['UPPER_VALUE']):
        raise ValueOutOfRangeException(param,
                                       data_type['LOWER_VALUE'],
                                       data_type['UPPER_VALUE'],
                                       data_type['UNITS'])


def validate_allowed_values(value, param, data_type):

    # Don't need to check the value is allowed if there are no
    # allowed values specified
    if 'ALLOWED_VALUES' not in data_type:
        return

    if value not in data_type['ALLOWED_VALUES']:
        raise ValueNotAllowedException(param,
                                       data_type['ALLOWED_VALUES'],
                                       data_type['UNITS'])


def get_value_or_quantity(model_val):
    # Get the value or the quantity from a model value

    # use the quantity, if it exists
    if hasattr(model_val, "quantity"):
        return model_val.quantity
    # or just use the unit-less value
    elif hasattr(model_val, "value"):
        return model_val.value
    # if neither of these attributes exist, throw an error
    else:
        raise ValueError(f'Invalid model. '
                         f'Expected ValueWithUnits or '
                         f'ValueWithoutUnits. '
                         f'Received {type(model_val)}.')


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
        print('in Value with units')
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
    def validate_t_int_or_sens_initialised(cls, field_values):
        # Validate that at least one of 't_int' and 'sensitivity'
        # has been initialised
        if field_values["t_int"].value == 0 and \
                field_values["sensitivity"].value == 0:
            raise ValueError("Please add either a sensitivity or an "
                             "integration time to your input.")
        return field_values

    @root_validator()
    @classmethod
    def validate_fields(cls, field_values):

        print('in UserInput validate_fields')
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

    def validate_update(self, value_to_update, new_value):
        """
        Custom validator called manually (i.e., not as part of the Pydantic
        framework), e.g., when one of the user input values is updated.
        """
        # TODO: will probably move this so that InstrumentSetup can call
        #       it and raise an error if an attempt is made to update one of the
        #       non-updatable fields

        try:
            self.validate_fields({value_to_update: new_value})
        except ValueError as e:
            raise e
        return self


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
    T_rx: ValueWithUnits = ValueWithUnits(value=TRx.DEFAULT_VALUE.value,
                                          unit=TRx.DEFAULT_UNIT.value)
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


# class CalculationInput(UserInput, InstrumentSetup):
class CalculationInput(BaseModel):
    """
    Input parameters used for the sensitivity calculation
    """

    user_input: UserInput = UserInput()
    instrument_setup: InstrumentSetup = InstrumentSetup()
    T_cmb: ValueWithUnits = \
        ValueWithUnits(value=TCmb.DEFAULT_VALUE.value,
                       unit=TCmb.DEFAULT_UNIT.value)

    @root_validator()
    @classmethod
    def flatten_values(cls, field_values):
        """
        Flatten the model so that it returns on parameters and their
        quantity/value as key-value pairs.
        NB: because this is a validator, it will modify the view of the
            data, although the underlying representation is still nested.
        """

        user_input = field_values['user_input']
        instrument_setup = field_values['instrument_setup']

        simplified_field_values = {}
        for elem in user_input:
            simplified_field_values[elem[0]] = get_value_or_quantity(elem[1])
        for elem in instrument_setup:
            simplified_field_values[elem[0]] = get_value_or_quantity(elem[1])
        simplified_field_values['T_cmb'] = \
            get_value_or_quantity(field_values['T_cmb'])

        return simplified_field_values


class DerivedParams(BaseModel):
    """
    Derived parameters, calculated from user input and instrument setup
    parameters.
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
    derived_params: DerivedParams

    def calculator_params_as_dict(self):
        """
        Flatten the structure of the object and return properties as a
        single-level dictionary
        """

        return dict((x, y) for x, y in
                    self.calculation_inputs) | dict((x, y)
                                                    for x, y
                                                    in self.derived_params)
