from atlast_sc.calculator import Calculator
from atlast_sc.parameter_setup import ParameterSetup
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.parameters.instrument_specific_parameters import InstrumentSpecificParameters
from atlast_sc.parameters.telescope_and_environment_parameters import TelescopeAndEnvironmentParameters
from atlast_sc.parameters.derived_parameters import DerivedParameters


class CalculatorFactory:
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
        return Calculator(param_setup)