from pydantic import BaseModel
import atlast_sc.data as data


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
                    "value": data.integration_time.default_value,
                    "unit": data.integration_time.default_unit,
                },
                "sensitivity": {
                    "value": data.sensitivity.default_value,
                    "unit": data.sensitivity.default_unit,
                },
                "bandwidth": {
                    "value": data.bandwidth.default_value,
                    "unit": data.bandwidth.default_unit,
                },
                "obs_freq": {
                    "value": data.obs_frequency.default_value,
                    "unit": data.obs_frequency.default_unit,
                },
                "elevation": {
                    "value": data.elevation.default_value,
                    "unit": data.elevation.default_unit,
                },
                "weather": {
                    "value": data.weather.default_value,
                },
                "n_pol": {
                    "value": data.n_pol.default_value,
                },
            }
        }
