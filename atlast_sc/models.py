from pydantic import BaseModel, root_validator
from astropy.units import Unit, Quantity


class ValueWithUnits(BaseModel):
    value: float
    unit: str

    @root_validator()
    @classmethod
    def to_quantity(cls, values):
        """
        Validate the unit and convert the value to an astropy Quantity object
        """

        # Ensure the unit string can be converted to a valid astropy Unit
        try:
            Unit(values["unit"])
        except ValueError as e:
            raise ValueError(e)

        # Convert the value to an astropy Quantity object
        values["value"] = values["value"] * Unit(values["unit"])
        return values

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
    t_int: ValueWithUnits = ValueWithUnits(value=100, unit="s")
    sensitivity: ValueWithUnits = ValueWithUnits(value=0.3, unit="mJy")
    bandwidth: ValueWithUnits = ValueWithUnits(value=7.5, unit="GHz")
    obs_freq: ValueWithUnits = ValueWithUnits(value=100, unit="GHz")
    n_pol: ValueWithoutUnits = ValueWithoutUnits(value=2)
    weather: ValueWithoutUnits = ValueWithoutUnits(value=50)
    elevation: ValueWithUnits = ValueWithUnits(value=30, unit="deg")

    @root_validator()
    @classmethod
    def validate_one_field_has_value(cls, field_values):
        """
        At least one of 't_int' and 'sensitivity' should be initialised
        """
        if field_values["t_int"].value == 0 and \
                field_values["sensitivity"].value == 0:
            raise ValueError("Please add either a sensitivity or an "
                             "integration time to your input.")
        return field_values


class InstrumentSetup(BaseModel):
    g: ValueWithoutUnits = ValueWithoutUnits(value=1)
    surface_rms: ValueWithUnits = ValueWithUnits(value=25, unit="micron")
    dish_radius: ValueWithUnits = ValueWithUnits(value=25, unit="m")
    T_amb: ValueWithUnits = ValueWithUnits(value=270, unit="K")
    T_rx: ValueWithUnits = ValueWithUnits(value=50, unit="K")
    eta_eff: ValueWithoutUnits = ValueWithoutUnits(value=0.80)
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
        Simplify the structure by only returning the value
        """
        simplified_field_values = {key: val.value for key, val
                                   in field_values.items()
                                   if hasattr(val, "value")}
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
