"""
Default values, default units, allowed units, allowed ranges and/or values
for the parameters used by the sensitivity calculator.
"""

from dataclasses import dataclass
import astropy.units as u
from atlast_sc.utils import DataHelper


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
    data_conversion: dict = None


integration_time = DataType(
    default_value=100,
    default_unit=str(u.s),
    lower_value=1,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(u.s), str(u.min), str(u.h)],
    data_conversion=DataHelper
    .data_conversion_factors(
        str(u.s),
        [str(u.s), str(u.min), str(u.h)]
    )
)

sensitivity = DataType(
    default_value=3.0,
    default_unit=str(u.mJy),
    lower_value=0,
    lower_value_is_floor=True,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(u.uJy), str(u.mJy), str(u.Jy)],
    data_conversion=DataHelper
    .data_conversion_factors(
        str(u.mJy),
        [str(u.uJy), str(u.mJy), str(u.Jy)]
    )
)

# TODO: include km/s. Will have to provide suitable conversion logic
bandwidth = DataType(
    default_value=100,
    default_unit=str(u.MHz),
    lower_value=0,
    lower_value_is_floor=True,
    upper_value=float('inf'),
    upper_value_is_ceil=True,
    units=[str(u.Hz), str(u.kHz), str(u.MHz), str(u.GHz)],
    data_conversion=DataHelper
    .data_conversion_factors(
        str(u.MHz),
        [str(u.Hz), str(u.kHz), str(u.MHz), str(u.GHz)]
    )
)

# Sky frequency of the observations
obs_frequency = DataType(
    default_value=100,
    default_unit=str(u.GHz),
    lower_value=35,
    upper_value=950,
    units=[str(u.GHz)]
)

# Number of polarisations being observed
n_pol = DataType(
    default_value=2,
    allowed_values=[1, 2]
)

# Relative Humidity (related to PWV, and ALMA weather bands as described
# in the 'Weather Conditions' section of the user guide
weather = DataType(
    default_value=25,
    lower_value=5,
    upper_value=95
)

# elevation of the target for calculating air mass
elevation = DataType(
    default_value=45,
    default_unit=str(u.deg),
    lower_value=25,
    upper_value=85,
    units=[str(u.deg)]
)

# Sideband Ratio
g = DataType(
    default_value=1
)

# surface smoothness, set to 25 micron to be consistent with OHB
# design requirements
surface_rms = DataType(
    default_value=25,
    default_unit=str(u.micron)
)

# radius of the primary mirror
dish_radius = DataType(
    default_value=25,
    default_unit=str(u.m),
    lower_value=1,
    upper_value=50,
    units=[str(u.m)]
)

# Average ambient Temperature
t_amb = DataType(
    default_value=270,
    default_unit=str(u.K)
)

# Forward Efficiency
eta_eff = DataType(
    default_value=0.8
)

# Illumination Efficiency
eta_ill = DataType(
    default_value=0.8
)

# Spillover Efficiency
eta_spill = DataType(
    default_value=0.95
)

# Lowered efficiency due to blocking
eta_block = DataType(
    default_value=0.94
)

# Polarisation Efficiency
eta_pol = DataType(
    default_value=0.99
)

# Temperature of the CMB
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
    'T_cmb': t_cmb,
}
