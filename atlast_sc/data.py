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
    lower_value=0,
    lower_value_is_floor=True,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(u.s), str(u.min), str(u.h)]
)

sensitivity = DataType(
    default_value=3.0,
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
    upper_value=50,
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

t_cmb = DataType(
    default_value=2.73,
    default_unit=str(u.K)
)

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
    'T_cmb': t_cmb,
}
