"""
Default values, default units, allowed units, allowed ranges and/or values
for the parameters used by the sensitivity calculator.
"""

from enum import Enum
import astropy.units as u

# TODO: check all of the defaults, ranges, and units


class BaseDataType(Enum):
    @classmethod
    def to_dict(cls):
        """
        Facilitates (and simplifies) access to class properties by providing
        a dict of property names and values as key-value pairs
        """
        return {p.name: p.value for p in cls}


####################################################################
# Data types and their labels, default values, default units, etc. #
####################################################################

class IntegrationTime(BaseDataType):
    DEFAULT_VALUE = 100
    DEFAULT_UNIT = str(u.s)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO: do we want to allow other time units?
    UNITS = [str(u.s)]


class Sensitivity(BaseDataType):
    DEFAULT_VALUE = 0.3
    DEFAULT_UNIT = str(u.mJy)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO confirm these allowable units are okay (additions?)
    UNITS = [str(unit) for unit in [u.uJy, u.mJy, u.Jy]]


class Bandwidth(BaseDataType):
    DEFAULT_VALUE = 7.5
    DEFAULT_UNIT = str(u.GHz)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO confirm these allowable units are okay (additions?)
    UNITS = [str(unit) for unit in [u.Hz, u.kHz, u.MHz, u.GHz]]


class ObsFrequency(BaseDataType):
    DEFAULT_VALUE = 100
    DEFAULT_UNIT = str(u.GHz)
    LOWER_VALUE = 35
    UPPER_VALUE = 950
    # TODO: Web client validation requests value in range 35-950 GHz, but do
    #  we want allow users to provide a value within the same range,
    #  but in different units?
    UNITS = [str(u.GHz)]


class NPol(BaseDataType):
    DEFAULT_VALUE = 2
    ALLOWED_VALUES = [1, 2]


class Weather(BaseDataType):
    DEFAULT_VALUE = 50
    LOWER_RANGE = 0
    # TODO: web client requests a value between 0 and 100%, but data
    #       validation restricts values to between 0 and 10. Clarify.
    UPPER_RANGE = 10


class Elevation(BaseDataType):
    DEFAULT_VALUE = 30
    DEFAULT_UNIT = str(u.deg)
    LOWER_VALUE = 5
    UPPER_VALUE = 90
    UNITS = [str(u.deg)]


class G(BaseDataType):
    DEFAULT_VALUE = 1


class SurfaceRMS(BaseDataType):
    DEFAULT_VALUE = 25
    DEFAULT_UNIT = str(u.micron)


class DishRadius(BaseDataType):
    DEFAULT_VALUE = 25
    DEFAULT_UNIT = str(u.m)
    # TODO get sensible range
    LOWER_VALUE = 0
    UPPER_VALUE = float('inf')
    # TODO: do we want to allow other length units?
    UNITS = [str(u.m)]


class TAmb(BaseDataType):
    DEFAULT_VALUE = 270
    DEFAULT_UNIT = str(u.K)


class TRx(BaseDataType):
    # TODO: this value should be calculated rather than set to a fixed value
    #   (function of obs_freq)
    DEFAULT_VALUE = 50
    DEFAULT_UNIT = str(u.K)


class EtaEff(BaseDataType):
    DEFAULT_VALUE = 0.8


class EtaIll(BaseDataType):
    # TODO: Docs say that eta_ill "defaults to value 0.63") What's the correct
    #  default?
    DEFAULT_VALUE = 0.8


class EtaSpill(BaseDataType):
    DEFAULT_VALUE = 0.95


class EtaBlock(BaseDataType):
    DEFAULT_VALUE = 0.94


class EtaPol(BaseDataType):
    DEFAULT_VALUE = 0.99


class EtaR(BaseDataType):
    DEFAULT_VALUE = 1


class EtaQ(BaseDataType):
    # TODO: What is eta_q and what default value should it have?
    #   Isn't documented and doesn't seem to be used anywhere
    DEFAULT_VALUE = 0.96


class TCmb(BaseDataType):
    DEFAULT_VALUE = 2.73
    DEFAULT_UNIT = str(u.K)


# Dictionary mapping parameters to their corresponding data type Enum
# dictionary representation
param_data_type_dicts = {
    't_int': IntegrationTime.to_dict(),
    'sensitivity': Sensitivity.to_dict(),
    'bandwidth': Bandwidth.to_dict(),
    'obs_freq': ObsFrequency.to_dict(),
    'n_pol': NPol.to_dict(),
    'weather': Weather.to_dict(),
    'elevation': Elevation.to_dict(),
    'g': G.to_dict(),
    'surface_rms': SurfaceRMS.to_dict(),
    'dish_radius': DishRadius.to_dict(),
    'T_amb': TAmb.to_dict(),
    'T_rx': TRx.to_dict(),
    'eta_eff': EtaEff.to_dict(),
    'eta_ill': EtaIll.to_dict(),
    'eta_spill': EtaSpill.to_dict(),
    'eta_block': EtaBlock.to_dict(),
    'eta_pol': EtaPol.to_dict(),
    'eta_r': EtaR.to_dict(),
    'eta_q': EtaQ.to_dict(),
}
