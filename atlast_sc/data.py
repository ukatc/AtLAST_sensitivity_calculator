"""
Default values, default units, allowed units, allowed ranges and/or values
for the parameters used by the sensitivity calculator.
"""

from dataclasses import dataclass
import astropy.units as u


@dataclass
class DataType:
    default_value: float = None
    default_unit: str = None
    lower_value: float = None
    lower_value_is_floor: bool = False
    upper_value: float = None
    upper_value_is_ceil: bool = False
    allowed_values: list = None
    units: list[str] = None


integration_time = DataType(
    default_value=100,
    default_unit=str(u.s),
    lower_value=1,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(u.s), str(u.min), str(u.h)]
)

sensitivity = DataType(
    default_value=0.3,
    default_unit=str(u.mJy),
    lower_value=0,
    lower_value_is_floor=True,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(unit) for unit in [u.uJy, u.mJy, u.Jy]]
)

# TODO: include km/s. Will have to provide suitable conversion logic
bandwidth = DataType(
    default_value=100,
    default_unit=str(u.MHz),
    lower_value=0,
    lower_value_is_floor=True,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(unit) for unit in [u.Hz, u.kHz, u.MHz, u.GHz]]
)

obs_frequency = DataType(
    default_value=100,
    default_unit=str(u.GHz),
    lower_value=35,
    upper_value=950,
    units=[str(u.GHz)]
)

n_pol = DataType(
    default_value=2,
    allowed_values=[1, 2]
)

weather = DataType(
    default_value=25,
    lower_value=5,
    upper_value=95
)

elevation = DataType(
    default_value=45,
    default_unit=str(u.deg),
    lower_value=25,
    upper_value=85,
    units=[str(u.deg)]
)

g = DataType(
    default_value=1
)

surface_rms = DataType(
    default_value=25,
    default_unit=str(u.micron)
)


dish_radius = DataType(
    default_value=25,
    default_unit=str(u.m),
    lower_value=1,
    upper_value=100,
    units=[str(u.m)]
)

t_amb = DataType(
    default_value=270,
    default_unit=str(u.K)
)

eta_eff = DataType(
    default_value=0.8
)

eta_ill = DataType(
    default_value=0.8
)

eta_spill = DataType(
    default_value=0.95
)

eta_block = DataType(
    default_value=0.94
)

eta_pol = DataType(
    default_value=0.99
)

eta_r = DataType(
    default_value=1
)

eta_q = DataType(
    default_value=0.96
)

t_cmb = DataType(
    default_value=2.73,
    default_unit=str(u.K)
)


####################################################################
# Data types and their labels, default values, default units, etc. #
####################################################################

# class IntegrationTime(BaseDataType):
#     DEFAULT_VALUE = 100
#     DEFAULT_UNIT = str(u.s)
#     LOWER_VALUE = 1
#     UPPER_VALUE = float('inf')
#     UPPER_VALUE_IS_CEIL = True
#     UNITS = [str(u.s), str(u.min), str(u.h)]
#
#
# class Sensitivity(BaseDataType):
#     DEFAULT_VALUE = 0.3
#     DEFAULT_UNIT = str(u.mJy)
#     LOWER_VALUE = 0
#     LOWER_VALUE_IS_FLOOR = True
#     UPPER_VALUE = float('inf')
#     UPPER_VALUE_IS_CEIL = True
#     UNITS = [str(unit) for unit in [u.uJy, u.mJy, u.Jy]]
#
#
# class Bandwidth(BaseDataType):
#     DEFAULT_VALUE = 100
#     DEFAULT_UNIT = str(u.MHz)
#     LOWER_VALUE = 0
#     LOWER_VALUE_IS_FLOOR = True
#     UPPER_VALUE = float('inf')
#     UPPER_VALUE_IS_CEIL = True
#     # TODO: include km/s. Will have to provide suitable conversion logic
#     UNITS = [str(unit) for unit in [u.Hz, u.kHz, u.MHz, u.GHz]]
#
#
# class ObsFrequency(BaseDataType):
#     DEFAULT_VALUE = 100
#     DEFAULT_UNIT = str(u.GHz)
#     LOWER_VALUE = 35
#     UPPER_VALUE = 950
#     UNITS = [str(u.GHz)]
#
#
# class NPol(BaseDataType):
#     DEFAULT_VALUE = 2
#     ALLOWED_VALUES = [1, 2]
#
#
# class Weather(BaseDataType):
#     DEFAULT_VALUE = 25
#     LOWER_VALUE = 5
#     UPPER_VALUE = 95
#
#
# class Elevation(BaseDataType):
#     DEFAULT_VALUE = 45
#     DEFAULT_UNIT = str(u.deg)
#     LOWER_VALUE = 25
#     UPPER_VALUE = 85
#     UNITS = [str(u.deg)]
#
#
# class G(BaseDataType):
#     DEFAULT_VALUE = 1
#
#
# class SurfaceRMS(BaseDataType):
#     DEFAULT_VALUE = 25
#     DEFAULT_UNIT = str(u.micron)
#
#
# class DishRadius(BaseDataType):
#     DEFAULT_VALUE = 25
#     DEFAULT_UNIT = str(u.m)
#     LOWER_VALUE = 1
#     UPPER_VALUE = 100
#     UNITS = [str(u.m)]
#
#
# class TAmb(BaseDataType):
#     DEFAULT_VALUE = 270
#     DEFAULT_UNIT = str(u.K)
#
#
# class EtaEff(BaseDataType):
#     DEFAULT_VALUE = 0.8
#
#
# class EtaIll(BaseDataType):
#     DEFAULT_VALUE = 0.8
#
#
# class EtaSpill(BaseDataType):
#     DEFAULT_VALUE = 0.95
#
#
# class EtaBlock(BaseDataType):
#     DEFAULT_VALUE = 0.94
#
#
# class EtaPol(BaseDataType):
#     DEFAULT_VALUE = 0.99
#
#
# class EtaR(BaseDataType):
#     DEFAULT_VALUE = 1
#
#
# class EtaQ(BaseDataType):
#     DEFAULT_VALUE = 0.96
#
#
# class TCmb(BaseDataType):
#     DEFAULT_VALUE = 2.73
#     DEFAULT_UNIT = str(u.K)


# Dictionary mapping parameters to their corresponding data type Enum
# dictionary representation
# param_data_type_dicts = {
#     't_int': IntegrationTime.to_dict(),
#     'sensitivity': Sensitivity.to_dict(),
#     'bandwidth': Bandwidth.to_dict(),
#     'obs_freq': ObsFrequency.to_dict(),
#     'n_pol': NPol.to_dict(),
#     'weather': Weather.to_dict(),
#     'elevation': Elevation.to_dict(),
#     'g': G.to_dict(),
#     'surface_rms': SurfaceRMS.to_dict(),
#     'dish_radius': DishRadius.to_dict(),
#     'T_amb': TAmb.to_dict(),
#     'eta_eff': EtaEff.to_dict(),
#     'eta_ill': EtaIll.to_dict(),
#     'eta_spill': EtaSpill.to_dict(),
#     'eta_block': EtaBlock.to_dict(),
#     'eta_pol': EtaPol.to_dict(),
#     'eta_r': EtaR.to_dict(),
#     'eta_q': EtaQ.to_dict(),
#     'T_cmb': TCmb.to_dict(),
# }

param_data_type_dicts = {
    't_int': integration_time,
    'sensitivity': sensitivity,
    'bandwidth': bandwidth,
    'obs_freq': obs_frequency,
    'n_pol': n_pol,
    'weather': weather,
    'elevation': elevation,
    'g': g,
    'surface_rms': surface_rms,
    'dish_radius': dish_radius,
    'T_amb': t_amb,
    'eta_eff': eta_eff,
    'eta_ill': eta_ill,
    'eta_spill': eta_spill,
    'eta_block': eta_block,
    'eta_pol': eta_pol,
    'eta_r': eta_r,
    'eta_q': eta_q,
    'T_cmb': t_cmb,
}
