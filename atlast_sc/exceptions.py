

class UnitException(ValueError):
    """
    Exception raised when a parameter is provided with invalid units
    """

    def __init__(self, parameter, expected_units, message=None):

        self.parameter = parameter
        self.expected_units = expected_units
        self.message = message \
            if message \
            else f"The parameter '{parameter}' " \
                 f"must have one of the following units: {expected_units}."

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
            else f"The parameter '{parameter}' " \
                 f"must be in the range {lower_value} " \
                 f"to {upper_value}" \
                 f"{'.' if not units else ' ' + str(units) + '.'}"

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
            else f"The parameter '{parameter}' " \
                 f"must have one of the following values: {allowed_values} " \
                 f"{'.' if not units else ' ' + str(units) + '.'}"

        super().__init__(self.message)
