Data model
**********

.. uml::

    @startuml data_model

    left to right direction

    class "<color:red>CalculatedValueInvalidWarning</color>" as exceptions.CalculatedValueInvalidWarning {
      message : str
      CalculatedValueInvalidWarning(message : str)
    }
    class "CalculationInput" as models.CalculationInput {
      T_cmb : ValueWithUnits
      instrument_setup : InstrumentSetup
      user_input : UserInput
      validate_fields(field_values)
      validate_update(value_to_update, new_value)
    }
    class "DataType" as data.DataType {
      allowed_values : list<float> | None
      data_conversion : dict | None
      default_unit : str | None
      default_value : str | None
      lower_value : float | None
      lower_value_is_floor : bool = False
      units : list<str> | None
      upper_value : float | None
      upper_value_is_ceil : bool = False
    }
    class "DerivedParams" as models.DerivedParams {
      T_atm : Quantity
      T_rx : Quantity
      T_sys : Quantity
      eta_a : float
      eta_s : float
      sefd : Quantity
      tau_atm : float
    }
    class "InstrumentSetup" as models.InstrumentSetup {
      T_amb : ValueWithUnits
      dish_radius : ValueWithUnits
      eta_block : ValueWithoutUnits
      eta_eff : ValueWithoutUnits
      eta_ill : ValueWithoutUnits
      eta_pol : ValueWithoutUnits
      eta_spill : ValueWithoutUnits
      g : ValueWithoutUnits
      surface_rms : ValueWithUnits
    }
    class "<color:red>UnitException</color>" as exceptions.UnitException {
      expected_units : str | list<str>
      message : str | None
      parameter : str
      UnitException(parameter : str,
      expected_units : str | list<str>, message : Optional[str])
    }
    class "UserInput" as models.UserInput {
      bandwidth : ValueWithUnits
      elevation : ValueWithUnits
      n_pol : ValueWithoutUnits
      obs_freq : ValueWithUnits
      sensitivity : ValueWithUnits
      t_int : ValueWithUnits
      weather : ValueWithoutUnits
      validate_t_int_or_sens_initialised(field_values)
    }
    class "Validator" as models.Validator {
      validate_allowed_values(value, param, data_type)
      validate_field(key, val)
      validate_in_range(value, param, data_type)
      validate_units(unit, param, data_type)
    }
    class "<color:red>ValueNotAllowedException</color>" as exceptions.ValueNotAllowedException {
      allowed_values : list<float>
      message : str | None
      parameter : str
      units : list<str> | None
      ValueNotAllowedException(parameter : str, allowed_values : list<str>,
      units : Optional[str], message : Optional[str])
    }
    class "<color:red>ValueOutOfRangeException</color>" as exceptions.ValueOutOfRangeException {
      lower_value : float | None
      message : str | None
      parameter : str
      units : str | None
      upper_value : float | None
      ValueOutOfRangeException(parameter : str, lower_value : float | None,
      upper_value : float | None, units: Optional[str], message : Optional[str])
    }
    class "<color:red>ValueTooHighException</color>" as exceptions.ValueTooHighException {
      message : str | None
      ValueTooHighException(parameter : str, upper_value : float,
      units : Optional[str], message : Optional[str])
    }
    class "<color:red>ValueTooLowException</color>" as exceptions.ValueTooLowException {
      message : str | None
      ValueTooLowException(parameter : str, lower_value : float,
      units : Optional[str], message : Optional[str])
    }
    class "ValueWithUnits" as models.ValueWithUnits {
      unit : str
      value : float
      validate_fields(field_values)
    }
    class "ValueWithoutUnits" as models.ValueWithoutUnits {
      value : float
    }

    models.InstrumentSetup --* models.CalculationInput
    models.UserInput --* models.CalculationInput
    models.Validator ..> models.CalculationInput
    exceptions --* models.Validator
    data.DataType ..> models.Validator
    data.DataType ..> models.CalculationInput
    data.DataType ..> models.UserInput
    data.DataType ..> models.InstrumentSetup
    models.ValueWithUnits --* models.CalculationInput
    models.ValueWithUnits --* models.UserInput
    models.ValueWithUnits --* models.InstrumentSetup
    models.ValueWithoutUnits --* models.CalculationInput
    models.ValueWithoutUnits --* models.UserInput
    models.ValueWithoutUnits --* models.InstrumentSetup
    exceptions.ValueTooHighException --|> exceptions.ValueOutOfRangeException
    exceptions.ValueTooLowException --|> exceptions.ValueOutOfRangeException
    @enduml