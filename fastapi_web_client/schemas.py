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
                    "value": data.IntegrationTime.DEFAULT_VALUE.value,
                    "unit": data.IntegrationTime.DEFAULT_UNIT.value,
                },
                "sensitivity": {
                    "value": data.Sensitivity.DEFAULT_VALUE.value,
                    "unit": data.Sensitivity.DEFAULT_UNIT.value,
                },
                "bandwidth": {
                    "value": data.Bandwidth.DEFAULT_VALUE.value,
                    "unit": data.Bandwidth.DEFAULT_UNIT.value,
                },
                "obs_freq": {
                    "value": data.ObsFrequency.DEFAULT_VALUE.value,
                    "unit": data.ObsFrequency.DEFAULT_UNIT.value,
                },
                "elevation": {
                    "value": data.Elevation.DEFAULT_VALUE.value,
                    "unit": data.Elevation.DEFAULT_UNIT.value,
                },
                "weather": {
                    "value": data.Weather.DEFAULT_VALUE.value,
                },
                "n_pol": {
                    "value": data.NPol.DEFAULT_VALUE.value,
                },
            }
        }
