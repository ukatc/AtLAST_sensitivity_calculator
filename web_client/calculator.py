import json, re
import math
import astropy.units as u
from dataclasses import asdict
from atlast_sc.calculator import Calculator
from atlast_sc.parameter_setup import ParameterSetup
from pydantic import ValidationError
from atlast_sc.core.data import Data


def do_calculation(user_input, calculation):
    """
    Perform the specified calculation (sensitivity or integration time)
    """
    try:
        calculator = _create_calculator(user_input)
    except UserInputError as e:
        raise e

    func = None
    match calculation:
        case "sensitivity":
            func = calculator.calculate_sensitivity
        case "integration_time":
            func = calculator.calculate_t_integration
        case _:
            # TODO: handle error
            pass
    
    calculated_param = func(update_calculator=False)

    value = calculated_param.value
    unit = str(calculated_param.unit)

    return {"value": value, "unit": unit}


def get_param_values_units():
    """
    Return the values, units, data conversion factors, etc. for each of the
    calculator input parameters (user input and instrument setup)
    """
    param_values_units = {
        param: asdict(data) for param, data in
        Data.param_data_type_dicts.items()
    }

    # convert 'inf' to very large number, otherwise the json encoder will
    # complain
    for param in param_values_units:
        for key, val in param_values_units[param].items():
            # print(key)
            if type(val) == float and math.isinf(val):
                param_values_units[param][key] = 100**10
    return param_values_units


def get_available_instruments():
    """
    Return a list of available instruments with Default always first
    """
    from atlast_sc.instruments.config import InstrumentConfig
    inst_config = InstrumentConfig()
    instrument_names = list(inst_config.instrument_classes.keys())
    # Sort the instruments, but put "Default" first
    sorted_instruments = sorted(instrument_names)
    if "Default" in sorted_instruments:
        sorted_instruments.remove("Default")
        sorted_instruments.insert(0, "Default")
    return sorted_instruments


def get_instrument_ranges(instrument_name):
    """
    Get the observing frequency and bandwidth ranges for a given instrument.
    
    :param instrument_name: name of the instrument (e.g., "Default", "Muscat", etc.)
    :return: dict with freq_range and bandwidth_range, or None if instrument not found
    """
    try:
        from atlast_sc.instruments.config import InstrumentConfig
        inst_config = InstrumentConfig()
        
        if instrument_name not in inst_config.instrument_classes:
            return None
        
        instrument = inst_config.instrument_classes[instrument_name]
        
        # Get frequency range from instrument
        freq_info = instrument.obs_freq_ranges_and_unit
        freq_ranges = freq_info.get('ranges', [])
        freq_unit = freq_info.get('unit', '')
        
        # Get bandwidth range from instrument
        bw_info = instrument.bandwidth_ranges_and_unit
        bw_ranges = bw_info.get('ranges', [])
        bw_unit = bw_info.get('unit', '')
        
        # Format the ranges as strings
        if freq_ranges:
            freq_range = re.findall(r"[\d.e]+", freq_ranges[0])
            freq_range_str = f"{freq_range[0]} - {freq_range[1]}"
        else:
            freq_range_str = "N/A"
            
        if bw_ranges:
            bw_range = re.findall(r"[\d.e]+", freq_ranges[0])
            bw_range_str = f"{bw_range[0]} - {bw_range[1]}"
        else:
            bw_range_str = "> 0"
            bw_unit = ""
        
        return {
            "freq_range": f"{freq_range_str} {freq_unit}",
            "bw_range": f"{bw_range_str} {bw_unit}"
        }
    except Exception as e:
        print(f"Error getting ranges for instrument {instrument_name}: {e}")
        return None


def get_recommended_instrument(obs_freq, bandwidth, bandwidth_unit=None):
    """
    Determine the recommended instrument based on observing frequency and bandwidth.
    Uses the existing ParameterSetup.find_applicable_instruments method for consistency.
    
    :param obs_freq: observing frequency (assumed in GHz)
    :param bandwidth: bandwidth value
    :param bandwidth_unit: bandwidth unit (e.g., 'MHz', 'GHz', default to 'MHz')
    :return: recommended instrument name
    """
    if not obs_freq or obs_freq == "":
        return "Default"
    
    try:
        obs_freq_ghz = float(obs_freq)
    except (ValueError, TypeError):
        return "Default"
    
    # Convert bandwidth to Hz based on the provided unit
    if bandwidth and bandwidth != "":
        try:
            bandwidth_val = float(bandwidth)
            
            # Default to MHz if no unit provided
            if not bandwidth_unit or bandwidth_unit == "":
                bandwidth_unit = "MHz"
            
            # Create a Quantity with the specified unit and convert to Hz
            bandwidth_quantity_temp = bandwidth_val * u.Unit(bandwidth_unit)
            bandwidth_hz = bandwidth_quantity_temp.to(u.Hz).value
        except (ValueError, TypeError):
            bandwidth_hz = 1e9  # Default 1 GHz
    else:
        bandwidth_hz = 1e9  # Default 1 GHz
    
    try:
        
        # Create a ParameterSetup instance to access find_applicable_instruments
        param_setup = ParameterSetup()
        
        # Create Quantity objects with appropriate units
        obs_freq_quantity = obs_freq_ghz * u.GHz
        bandwidth_quantity = bandwidth_hz * u.Hz
        
        # Use the existing method to find the applicable instrument
        recommended = param_setup.find_applicable_instruments(
            obs_freq_quantity,
            bandwidth_quantity,
            param_setup.instrument_obs_freqs,
            param_setup.instrument_bandw_vals
        )
        
        return recommended
    except Exception as e:
        # If there's any error, return Default
        print(f"Error determining instrument: {e}")
        return "Default"


def _create_calculator(user_input):
    """
    Create a calculator object with the specified user input and apply
    the currently selected instrument if one has been set.
    """
    try:
        calculator = Calculator(user_input)
    except ValidationError as e:
        message = json.loads(e.json())[0]["msg"]
        raise UserInputError(message)
    
    # Apply the selected instrument if one has been set
    try:
        from web_client import main
        if main.selected_instrument:
            calculator.chosen_instrument = main.selected_instrument
    except Exception as e:
        # If there's any error applying the instrument, log it but continue
        print(f"Warning: Could not apply selected instrument: {e}")

    return calculator


class UserInputError(ValueError):

    def __init__(self, message):
        self.message = message

        super().__init__(message)
