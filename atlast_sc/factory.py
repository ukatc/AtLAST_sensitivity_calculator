from atlast_sc.calculator import Calculator
from atlast_sc.parameter_setup import ParameterSetup
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.parameters.instrument_specific_parameters import InstrumentSpecificParameters
from atlast_sc.parameters.telescope_and_environment_parameters import TelescopeAndEnvironmentParameters
from atlast_sc.parameters.derived_parameters import DerivedParameters


class CalculatorFactory:
    # def __init__(self, user_input={}, instrument_setup={}, telescope_and_environment= {}, finetune=False):
    def __init__(self, user_input={}, instrument_name="default"):
        if user_input:
            self.calculator = self._create_calculator(ParameterSetup(user_input=user_input))
        else: # use the default values
            self.calculator = self._create_calculator(ParameterSetup())

    #####################
    # Protected methods #
    #####################
    @staticmethod
    def _create_calculator(param_setup):
        default_uip = UserInputParameters(param_setup)
        default_isp = InstrumentSpecificParameters(param_setup)
        default_tep = TelescopeAndEnvironmentParameters(param_setup)
        default_dp_model = default_uip._calculate_derived_parameters()
        default_dp = DerivedParameters(default_dp_model)
        return Calculator(param_setup, default_uip, default_isp, default_tep, default_dp)