"""
Default values, default units, allowed units, allowed ranges and/or values
for the parameters used by the sensitivity calculator.

Validators to check that data models have valid values and unts.
"""

from enum import Enum
import astropy.units as u

# TODO: check all of the defaults, ranges, and units


class IntegrationTime(Enum):
    PARAM_LABEL = 't_int'
    DEFAULT_VALUE = 100
    DEFAULT_UNIT = str(u.s)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO: do we want to allow other time units?
    UNITS = [str(u.s)]


class Sensitivity(Enum):
    PARAM_LABEL = 'sensitivity'
    DEFAULT_VALUE = 0.3
    DEFAULT_UNIT = str(u.mJy)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO confirm these allowable units are okay (additions?)
    UNITS = [str(unit) for unit in [u.uJy, u.mJy, u.Jy]]


class Bandwidth(Enum):
    PARAM_LABEL = 'bandwidth'
    DEFAULT_VALUE = 7.5
    DEFAULT_UNIT = str(u.GHz)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO confirm these allowable units are okay (additions?)
    UNITS = [str(unit) for unit in [u.Hz, u.kHz, u.MHz, u.GHz]]


class ObsFrequency(Enum):
    PARAM_LABEL = 'obs_freq'
    DEFAULT_VALUE = 100
    DEFAULT_UNIT = str(u.GHz)
    LOWER_VALUE = 35
    UPPER_VALUE = 950
    # TODO: Web client validation requests value in range 35-950 GHz, but do
    #  we want allow users to provide a value within the same range,
    #  but in different units?
    UNITS = [str(u.GHz)]


class NPol(Enum):
    PARAM_LABEL = 'n_pol'
    DEFAULT_VALUE = 2
    ALLOWED_VALUES = [1, 2]


class Weather(Enum):
    PARAM_LABEL = 'weather'
    DEFAULT_VALUE = 50
    LOWER_RANGE = 0
    # TODO: web client requests a value between 0 and 100%, but data
    #       validation restricts values to between 0 and 10. Clarify.
    UPPER_RANGE = 10


class Elevation(Enum):
    PARAM_LABEL = 'elevation'
    DEFAULT_VALUE = 30
    DEFAULT_UNIT = str(u.deg)
    LOWER_VALUE = 5
    UPPER_VALUE = 90
    UNITS = [str(u.deg)]
