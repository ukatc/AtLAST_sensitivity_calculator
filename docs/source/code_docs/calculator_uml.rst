Calculator
^^^^^^^^^^

.. uml::

    @startuml calculator

    left to right direction

    class "AtmosphereParams" as derived_groups.AtmosphereParams {
      AtmosphereParams()
      calculate_atmospheric_temperature(obs_freq : Quantity, weather: float) : Quantity
      calculate_tau_atm(obs_freq : Quantity, weather : float, elevation : Quantity) : float
    }
    class "Calculator" as calculator.Calculator {
      bandwidth : Quantity
      dish_radius : Quantity
      elevation : Quantity
      eta_a : float
      eta_block : float
      eta_eff : float
      eta_ill : float
      eta_pol : float
      eta_s : float
      eta_spill : float
      g : float
      n_pol : float
      obs_freq : Quantity
      sefd : Quantity
      sensitivity : Quantity
      surface_rms : Quantity
      t_int : Quantity
      T_amb : Quantity
      T_atm : Quantity
      T_cmb : Quantity
      T_rx : Quantity
      T_sys  : Quantity
      tau_atm : float
      weather : float
      user_input : UserInput
      calculation_inputs : CalculationInput
      derived_parameters : DerivedParams
      instrument_setup : InstrumentSetup
      Calculator(user_input: dict, instrument_setup: dict)
      calculate_sensitivity(t_int, update_calculator): Quantity
      calculate_t_integration(sensitivity, update_calculator) : Quantity
      reset()
    }
    class "Config" as calculator.Config {
      calculation_inputs : CalculationInput
      instrument_setup : InstrumentSetup
      user_input : UserInput
      Config(user_input: Optiona[dict], instrument_setup: Optional[dict])
      reset()
    }
    class "Efficiencies" as derived_groups.Efficiencies {
      eta_a : float
      eta_s : float
      Efficiencies(obs_freq : Quantity, surface_rms : Quantity,
      eta_ill : float, eta_spill : float, eta_block : float, eta_pol : float)
    }
    class "Temperatures" as derived_groups.Temperatures {
      T_rx : Quantity
      T_sys : Quantity
      Temperatures(obs_freq : Quantity, T_cmb : Quantity, T_amb : Quantity,
      g : float, eta_eff : float, T_atm : Quantity, tau_atm: float)
    }
    derived_groups.Efficiencies --* calculator.Calculator
    derived_groups.Temperatures --* calculator.Calculator
    derived_groups.AtmosphereParams --* calculator.Calculator
    models.CalculationInput --* calculator.Config
    models.InstrumentSetup --* calculator.Config
    models.UserInput --* calculator.Config
    calculator.Calculator *-- models.DerivedParams
    models.CalculationInput ..> calculator.Calculator
    models.InstrumentSetup ..> calculator.Calculator
    models.UserInput ..> calculator.Calculator
    calculator.Calculator *-- calculator.Config
    @enduml