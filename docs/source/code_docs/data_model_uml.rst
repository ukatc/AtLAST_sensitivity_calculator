Data model
^^^^^^^^^^

.. uml::

    @startuml data_model

    left to right direction

    class "CalculationInput" as models.CalculationInput {
      T_cmb : ValueWithUnits
      instrument_setup : InstrumentSetup
      user_input : UserInput
      validate_fields(field_values) : dict
      validate_value(value_to_update, new_value) : dict
    }
    class "Data" as data.Data {
      bandwidth : DataType
      dish_radius : DataType
      elevation : DataType
      eta_block : DataType
      eta_eff : DataType
      eta_ill : DataType
      eta_pol : DataType
      eta_spill : DataType
      g : DataType
      integration_time : DataType
      n_pol : DataType
      obs_frequency : DataType
      sensitivity : DataType
      surface_rms : DataType
      t_amb : DataType
      t_cmb : DataType
      weather : DataType
      param_data_type_dicts : dict
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
    class "Validator" as data.Validator {
      {static} validate_allowed_values(value, param, data_type)
      {static} validate_field(key, val)
      {static} validate_in_range(value, param, data_type)
      {static} validate_units(unit, param, data_type)
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
    data.Validator ..> models.CalculationInput
    data.DataType --+ data.Data
    data.Data ..> data.Validator
    data.Data ..> models.CalculationInput
    data.Data ..> models.UserInput
    data.Data ..> models.InstrumentSetup
    models.ValueWithUnits --* models.CalculationInput
    models.ValueWithUnits --* models.UserInput
    models.ValueWithUnits --* models.InstrumentSetup
    models.ValueWithoutUnits --* models.CalculationInput
    models.ValueWithoutUnits --* models.UserInput
    models.ValueWithoutUnits --* models.InstrumentSetup
    @enduml