Utilities
*********

.. uml::

    @startuml utils

    left to right direction

    class "FileHelper" as utils.FileHelper {
      {static} read_from_file(path : str, file_name : str)
      {static} write_to_file(calculator : Calculator, path : str, file_name : str, file_type)
    }
    class "DataHelper" as utils.DataHelper {
      {static} data_conversion_factors(default_unit : str, allowed_units : list<str>)
    }
    class "Decorators" as utils.Decorators {
      {static} validate_and_update_params(func)
      {static} validate_update(func)
    }
    utils.FileHelper <.. calculator.Calculator
    utils.Decorators ..> calculator.Calculator
    utils.DataHelper ..> data.Data
    @enduml