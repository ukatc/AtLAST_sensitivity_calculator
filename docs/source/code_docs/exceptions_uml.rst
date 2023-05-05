Exceptions
**********

.. uml::

    @startuml exceptions

    left to right direction

    class "<color:red>CalculatedValueInvalidWarning</color>" as exceptions.CalculatedValueInvalidWarning {
      message : str
      CalculatedValueInvalidWarning(message : str)
    }
    class "<color:red>UnitException</color>" as exceptions.UnitException {
      expected_units : str | list<str>
      message : str | None
      parameter : str
      UnitException(parameter : str,
      expected_units : str | list<str>, message : Optional[str])
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

    exceptions.ValueTooHighException --|> exceptions.ValueOutOfRangeException
    exceptions.ValueTooLowException --|> exceptions.ValueOutOfRangeException
    exceptions --* data.Validator
    @enduml