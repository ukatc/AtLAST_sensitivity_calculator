from atlast_sc.calculator import Calculator
from atlast_sc.parameter_setup import ParameterSetup

class CalculatorFactory:
    def __init__(self, user_input={}):
        if user_input:
            self.calculator = self._create_calculator(param_setup=ParameterSetup(user_input=user_input))
        else: # use the default values
            self.calculator = self._create_calculator(param_setup=ParameterSetup())

    #####################
    # Protected methods #
    #####################
    @staticmethod
    def _create_calculator(param_setup):
        return Calculator(param_setup)