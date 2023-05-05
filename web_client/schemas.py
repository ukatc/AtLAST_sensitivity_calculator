from pydantic import BaseModel
from atlast_sc.data import Data


class APIUserInput(BaseModel):
    """
    A convenience model that allows us to specify both the required data
    and value and unit hints.
    (NB: We're not able to take advantage of the UserInput model in the
     atlast_sc.models package because of recursion issues. Not clear why
     this is a problem.)
    """

    t_int: dict
    sensitivity: dict
    bandwidth: dict
    obs_freq: dict
    elevation: dict
    weather: dict
    n_pol: dict

    class Config:
        schema_extra = {
            "example": {
                "t_int": {
                    "value": Data.integration_time.default_value,
                    "unit": Data.integration_time.default_unit,
                },
                "sensitivity": {
                    "value": Data.sensitivity.default_value,
                    "unit": Data.sensitivity.default_unit,
                },
                "bandwidth": {
                    "value": Data.bandwidth.default_value,
                    "unit": Data.bandwidth.default_unit,
                },
                "obs_freq": {
                    "value": Data.obs_frequency.default_value,
                    "unit": Data.obs_frequency.default_unit,
                },
                "elevation": {
                    "value": Data.elevation.default_value,
                    "unit": Data.elevation.default_unit,
                },
                "weather": {
                    "value": Data.weather.default_value,
                },
                "n_pol": {
                    "value": Data.n_pol.default_value,
                },
            }
        }
