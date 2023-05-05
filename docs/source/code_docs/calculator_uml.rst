Calculator
**********

.. uml::

    @startuml calculator

    left to right direction


    class "AtmosphereParams" as atmosphere_params.AtmosphereParams {
      T_atm : Quantity
      tau_atm : float
      AtmosphereParams(obs_freq : Quantity, weather : float,
      elevation : Quantity)
    }
    class "CalculationInput" as models.CalculationInput {
      T_cmb : ValueWithUnits
      instrument_setup : InstrumentSetup
      user_input : UserInput
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
    class "DerivedParams" as models.DerivedParams {
      T_atm : Quantity
      T_rx : Quantity
      T_sys : Quantity
      eta_a : float
      eta_s : float
      sefd : Quantity
      tau_atm : float
    }
    class "Efficiencies" as efficiencies.Efficiencies {
      eta_a : float
      eta_s : float
      Efficiencies(obs_freq : Quantity, surface_rms : Quantity,
      eta_ill : float, eta_spill : float, eta_block : float, eta_pol : float)
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
    class "Temperatures" as temperatures.Temperatures {
      T_rx : Quantity
      T_sys : Quantity
      Temperatures(obs_freq : Quantity, T_cmb : Quantity, T_amb : Quantity,
      g : float, eta_eff : float, atmosphere_params : AtmosphereParams)
    }
    class "UserInput" as models.UserInput {
      bandwidth : ValueWithUnits
      elevation : ValueWithUnits
      n_pol : ValueWithoutUnits
      obs_freq : ValueWithUnits
      sensitivity : ValueWithUnits
      t_int : ValueWithUnits
      weather : ValueWithoutUnits
    }
    efficiencies.Efficiencies --* calculator.Calculator
    temperatures.Temperatures --* calculator.Calculator
    atmosphere_params.AtmosphereParams --* calculator.Calculator
    models.CalculationInput --* calculator.Config
    models.InstrumentSetup --* calculator.Config
    models.UserInput --* calculator.Config
    calculator.Calculator *-- models.DerivedParams
    models.CalculationInput ..> calculator.Calculator
    models.InstrumentSetup ..> calculator.Calculator
    models.UserInput ..> calculator.Calculator
    calculator.Calculator *-- calculator.Config
    @enduml