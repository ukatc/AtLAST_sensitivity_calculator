from pydantic import BaseModel, BaseSettings, validator, root_validator
from astropy.units import Unit


class ValueWithUnits(BaseModel):
    value: int
    unit: str

    @classmethod
    @validator('unit')
    def unit_must_be_valid(cls, unit):
        """
        Ensure the unit string can be converted to a valid astropy Unit
        """
        # TODO: validator not being called?
        print('i am validating....')
        try:
            Unit(unit)
        except ValueError as e:
            raise ValueError(e)
        return unit


class ValueWithoutUnits(BaseModel):
    value: int


class VariableInput(BaseModel):
    """
    Definition of the variable input to the sensitivity calculation.
    The user is expected to provide this input during normal usage.
    Default values are provided for convenience.
    """
    # TODO: simplify
    t_int: ValueWithUnits = ValueWithUnits(**{"value": 70, "unit": "s"})
    sensitivity: ValueWithUnits = ValueWithUnits(**{"value": 0, "unit": "mJy"})
    bandwidth: ValueWithUnits = ValueWithUnits(**{"value": 7.5, "unit": "GHz"})
    obs_freq: ValueWithUnits = ValueWithUnits(**{"value": 100, "unit": "GHz"})
    n_pol: ValueWithoutUnits = ValueWithoutUnits(**{"value": 2})
    weather: ValueWithoutUnits = ValueWithoutUnits(**{"value": 50})
    elevation: ValueWithUnits = ValueWithUnits(**{"value": 30, "unit": "deg"})

    @classmethod
    @root_validator()
    def validate_one_field_has_value(cls, field_values):
        """pydant
        Exactly one of 't_int' and 'sensitivity' should be initialised
        """

        print('t_int', field_values["t_int"])
        print('sens', field_values["sensitivity"])

        if field_values["t_int"] and field_values["sensitivity"]:
            print('they are both set')

        if not (field_values["t_int"] or field_values["sensitivity"]):
            print('neither value is set')

        if (field_values["t_int"] and field_values["sensitivity"]) \
                or not (field_values["t_int"] or field_values["sensitivity"]):
            # TODO: split into two different tests?
            print("i got here")
            raise ValueError("Please add either a sensitivity *or* an integration time to your input. MY MESSAGE")

        return field_values


class InstrumentSetup(BaseModel):
    # TODO: simplify
    g: ValueWithoutUnits = ValueWithoutUnits(**{"value": 1})
    surface_rms: ValueWithUnits = ValueWithUnits(**{"value": 25, "unit": "micron"})
    dish_radius: ValueWithUnits = ValueWithUnits(**{"value": 25, "unit": "m"})
    T_amb: ValueWithUnits = ValueWithUnits(**{"value": 270, "unit": "K"})
    T_rx: ValueWithUnits = ValueWithUnits(**{"value": 50, "unit": "K"})
    eta_eff: ValueWithoutUnits = ValueWithoutUnits(**{"value": 0.80})
    eta_ill: ValueWithoutUnits = ValueWithoutUnits(**{"value": 0.80})
    # TODO: What is eta_q and what default value should it have?
    eta_q: ValueWithoutUnits = ValueWithoutUnits(**{"value": 0.96})
    eta_spill: ValueWithoutUnits = ValueWithoutUnits(**{"value": 0.95})
    eta_block: ValueWithoutUnits = ValueWithoutUnits(**{"value": 0.94})
    eta_pol: ValueWithoutUnits = ValueWithoutUnits(**{"value": 0.99})
    eta_r: ValueWithoutUnits = ValueWithoutUnits(**{"value": 1})


class CalculationInput(VariableInput, InstrumentSetup):
    variable_input: VariableInput = VariableInput()
    instrument_setup: InstrumentSetup = InstrumentSetup()
    T_cmb: ValueWithUnits = ValueWithUnits(**{"value": 2.73, "unit": "K"})
