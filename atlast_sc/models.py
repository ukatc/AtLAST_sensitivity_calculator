from pydantic import BaseModel, root_validator
from astropy.units import Unit, Quantity
from atlast_sc.exceptions import ValueOutOfRangeException
from atlast_sc.data import Data, Validator


def model_str_rep(model):
    """
    Creates a "pretty" string representation of the model

    :param model: The model to prettify
    :type model: subclass of BaseModel
    """
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
        ValueWithUnits(value=Data.integration_time.default_value,
                       unit=Data.integration_time.default_unit)
    sensitivity: ValueWithUnits = \
        ValueWithUnits(value=Data.sensitivity.default_value,
                       unit=Data.sensitivity.default_unit)
    bandwidth: ValueWithUnits = \
        ValueWithUnits(value=Data.bandwidth.default_value,
                       unit=Data.bandwidth.default_unit)
    obs_freq: ValueWithUnits = \
        ValueWithUnits(value=Data.obs_frequency.default_value,
                       unit=Data.obs_frequency.default_unit)
    n_pol: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.n_pol.default_value)
    weather: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.weather.default_value)
    elevation: ValueWithUnits = \
        ValueWithUnits(value=Data.elevation.default_value,
                       unit=Data.elevation.default_unit)

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
    g: ValueWithoutUnits = ValueWithoutUnits(value=Data.g.default_value)
    surface_rms: ValueWithUnits = \
        ValueWithUnits(value=Data.surface_rms.default_value,
                       unit=Data.surface_rms.default_unit)
    dish_radius: ValueWithUnits = \
        ValueWithUnits(value=Data.dish_radius.default_value,
                       unit=Data.dish_radius.default_unit)
    T_amb: ValueWithUnits = \
        ValueWithUnits(value=Data.t_amb.default_value,
                       unit=Data.t_amb.default_unit)
    eta_eff: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.eta_eff.default_value)
    eta_ill: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.eta_ill.default_value)
    eta_spill: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.eta_spill.default_value)
    eta_block: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.eta_block.default_value)
    eta_pol: ValueWithoutUnits = \
        ValueWithoutUnits(value=Data.eta_pol.default_value)

    def __str__(self):
        return model_str_rep(self)


class CalculationInput(BaseModel):
    """
    Input parameters used for the sensitivity calculation
    """

    user_input: UserInput = UserInput()
    instrument_setup: InstrumentSetup = InstrumentSetup()
    T_cmb: ValueWithUnits = \
        ValueWithUnits(value=Data.t_cmb.default_value,
                       unit=Data.t_cmb.default_unit)

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
