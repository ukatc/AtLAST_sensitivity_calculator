
class CalculatedValueInvalidWarning(UserWarning):
    """
    Warning raised when a calculated value is not valid, e.g., because it
    falls outside its permitted range.
    """

    def __init__(self, message):
        """
        :param message: the warning message to display
        :type message: str
        """
        self.message = message


class UnitException(ValueError):
    """
    Exception raised when a parameter is provided with invalid units
    """

    def __init__(self, parameter, expected_units, message=None):

        self.parameter = parameter
        self.expected_units = expected_units
        self.message = message if message else \
            f"The parameter '{self.parameter}' must have one of " \
            f"the following units: {self.expected_units}."

        super().__init__(self.message)


class ValueOutOfRangeException(ValueError):
    """
    Exception raised when a parameter is not within a certain range
    """

    def __init__(self, parameter, lower_value, upper_value, units=None,
                 message=None):

        self.parameter = parameter
        self.lower_value = lower_value
        self.upper_value = upper_value
        self.units = units
        self.message = message \
            if message \
            else f"The parameter '{self.parameter}' " \
                 f"must be in the range {self.lower_value} " \
                 f"to {self.upper_value}" \
                 f"{'.' if not self.units else ' ' + str(self.units) + '.'}"

        super().__init__(self.message)


class ValueTooLowException(ValueOutOfRangeException):

    def __init__(self, parameter, lower_value, units=None, message=None):

        self.message = message if message \
            else f"The parameter '{parameter}' " \
                 f"must be greater than {lower_value}" \
                 f"{'.' if not units else ' ' + str(units) + '.'}"

        super().__init__(parameter, lower_value, None, units, self.message)


class ValueTooHighException(ValueOutOfRangeException):

    def __init__(self, parameter, upper_value, units=None, message=None):
        self.message = message if message \
            else f"The parameter '{parameter}' " \
                 f"must be less than {upper_value}" \
                 f"{'.' if not units else ' ' + str(units) + '.'}"

        super().__init__(parameter, None, upper_value, units, self.message)


class ValueNotAllowedException(ValueError):
    """
    Exception raised when a parameter in not one of the allowed values
    """

    def __init__(self, parameter, allowed_values, units=None,
                 message=None):
        self.parameter = parameter
        self.allowed_values = allowed_values
        self.units = units
        self.message = message \
            if message\
            else f"The parameter '{self.parameter}' " \
                 f"must have one of the following " \
                 f"values: {self.allowed_values}" \
                 f"{'.' if not self.units else ' ' + str(self.units) + '.'}"

        super().__init__(self.message)
