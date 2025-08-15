from atlast_sc.calculator import Calculator
from atlast_sc.config import Config
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.parameters.instrument_setup_parameters import InstrumentSetupParameters
from atlast_sc.models import UserInput

class CalculatorFactory:
    def __init__(self, user_input={}, instrument_setup={}, finetune=False):
        self._finetune = finetune

        # Make sure the user input doesn't contain any unexpected parameter
        # names
        self._check_input_param_names(user_input)

        # Store the input parameters used to initialise the calculator
        self._config = Config(user_input, instrument_setup)
        # Calculate the derived parameters used in the calculation
        self._uip = UserInputParameters(self._config)
        self._isp = InstrumentSetupParameters(self._config)
        
        self.calculator = Calculator(self._config, self._uip, self._isp, self._finetune)

    #####################
    # Protected methods #
    #####################

    @staticmethod
    def _check_input_param_names(user_input):
        """
        Validates the user input parameters (just the names; value validation
        is handled by the model)

        :param user_input: Dictionary containing user-defined input parameters
        :type user_input: dict
        """

        test_model = UserInput()

        for param in user_input:
            if param not in test_model.__dict__:
                raise ValueError(f'"{param}" is not a valid input parameter')