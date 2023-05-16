import math
from dataclasses import dataclass
import astropy.units as u
from astropy.units import Unit, Quantity
from atlast_sc.utils import DataHelper
from atlast_sc.exceptions import UnitException, ValueOutOfRangeException,\
    ValueNotAllowedException, ValueTooHighException, ValueTooLowException


class Data:
    """
    Default values, default units, allowed units, allowed ranges and/or values
    for the parameters used by the sensitivity calculator.
    """

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

        def __post_init__(self):
            # Make sure the default value is not infinity
            assert not math.isinf(self.default_value)
            # If there's a lower value, make sure there's also an upper value
            if self.lower_value:
                assert self.upper_value is not None
                # Make sure the default value is within the permitted range
                if not self.lower_value_is_floor:
                    assert self.default_value >= self.lower_value
                else:
                    assert self.default_value > self.lower_value
                # (Handle infinity differently)
                if not math.isinf(self.upper_value):
                    # Make sure the upper value is greater than the lower value
                    assert self.upper_value > self.lower_value
                    if not self.upper_value_is_ceil:
                        assert self.default_value <= self.upper_value
                    else:
                        assert self.default_value < self.upper_value
                # Make sure an allowed values has not also been specified
                assert self.allowed_values is None
                # Make sure the lower value is not infinity
                assert not math.isinf(self.lower_value)
            # If there's an upper value, make sure there's also a lower value
            if self.upper_value:
                assert self.lower_value is not None
                # Make sure an allowed values has not also been specified
                assert self.allowed_values is None
            if self.units:
                # Make sure all the units are valid astropy units
                Unit(self.default_unit)
                for unit in self.units:
                    Unit(unit)
                # Make sure the default unit is in the list of allowed units
                assert self.default_unit in self.units
            # If a list of allowed values has been provided, make sure the
            # default value is one of these
            if self.allowed_values:
                assert self.default_value in self.allowed_values

            # If the data type has a list of allowed units, evaluate the data
            # conversion factors between allowed units and the default unit
            if self.units:
                self.data_conversion = DataHelper.data_conversion_factors(
                    self.default_unit,
                    self.units
                )

    integration_time = DataType(
        default_value=100,
        default_unit=str(u.s),
        lower_value=1,
        upper_value=float('inf'),
        upper_value_is_ceil=True,
        units=[str(u.s), str(u.min), str(u.h)],
    )

    sensitivity = DataType(
        default_value=3.0,
        default_unit=str(u.mJy),
        lower_value=0,
        lower_value_is_floor=True,
        upper_value=float('inf'),
        upper_value_is_ceil=True,
        units=[str(u.uJy), str(u.mJy), str(u.Jy)],
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

    # Elevation of the target for calculating air mass
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


class Validator:
    """
    Class providing custom validation functions
    """

    @staticmethod
    def validate_field(key, val):

        data_type = Data.param_data_type_dicts[key]

        # Validate units on Quantities
        if isinstance(val, Quantity):
            try:
                Validator.validate_units(val.unit, key, data_type)
            except UnitException as e:
                raise e

        # Validate value is allowed
        if isinstance(val, Quantity):
            # Convert the value to the default units and extract the value
            # to be validated
            value_to_validate = \
                val.to(Unit(data_type.default_unit)).value
        else:
            value_to_validate = val

        try:
            Validator.validate_allowed_values(value_to_validate,
                                              key, data_type)
        except ValueNotAllowedException as e:
            raise e

        # Validate value is in permitted range
        try:
            Validator.validate_in_range(value_to_validate,
                                        key, data_type)
        except ValueOutOfRangeException as e:
            raise e

    @staticmethod
    def validate_units(unit, param, data_type):

        # Don't need to check the units if the data type is unit-less
        if data_type.units is None:
            return

        if unit not in data_type.units:
            raise UnitException(param, data_type.units)

    @staticmethod
    def validate_in_range(value, param, data_type):

        # Don't need to check the value is in the permitted range if
        #   there is no range specified
        if data_type.lower_value is None:
            return

        # If the lower value is a floor value, make sure the provided value
        # is greater than this
        if data_type.lower_value_is_floor:
            if value <= data_type.lower_value:
                raise ValueTooLowException(param, data_type.lower_value,
                                           data_type.default_unit)

        # Do a special check for infinity (unlikely scenario, but not
        # impossible...)
        if math.isinf(value):
            raise ValueTooHighException(param, data_type.upper_value,
                                        data_type.default_unit)

        # If the upper value is a ceiling value, make sure the provided value
        # is less than
        if data_type.upper_value_is_ceil:
            if value >= data_type.upper_value:
                raise ValueTooHighException(param, data_type.upper_value,
                                            data_type.default_unit)

        if not (data_type.lower_value <= value <= data_type.upper_value):
            raise ValueOutOfRangeException(param,
                                           data_type.lower_value,
                                           data_type.upper_value,
                                           data_type.default_unit)

    @staticmethod
    def validate_allowed_values(value, param, data_type):

        # Don't need to check the value is allowed if there are no
        # allowed values specified
        if data_type.allowed_values is None:
            return

        if value not in data_type.allowed_values:
            raise ValueNotAllowedException(param,
                                           data_type.allowed_values,
                                           data_type.default_unit)
