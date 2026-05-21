from contextlib import contextmanager
import re
from atlast_sc.utils import FileHelper

from atlast_sc.instruments.config import InstrumentConfig
from atlast_sc.instruments.classes.Default import Default

@contextmanager
def does_not_raise():
    # Utility for checking that an exception is NOT raised
    yield

def create_default_inst_class():
    default_inst_data = FileHelper.read_instrument_yaml_file("Default")
    default_inst_module = Default(default_inst_data)
    return default_inst_module

def get_instrument_modules():
    # Get instrument config 
    inst_config = InstrumentConfig()
    # Get loaded instrument classes
    return inst_config.instrument_classes

def find_chosen_instrument(obs_freq, bandwidth):
      # Look at obs_freq and bandwidth values
        obs_freq = obs_freq.value
        bandwidth = bandwidth.value
        inst_modules = get_instrument_modules()

        # See which instrument those values correspond to
        instrument_obs_freqs = {} # Instrument specific observing frequency ranges
        instrument_bandw_vals = {} # Instrument specific bandwidth value ranges
        for inst_name, inst_module in inst_modules.items():
            instrument_obs_freqs[inst_name] = inst_module.obs_freq_ranges_and_unit
            instrument_bandw_vals[inst_name] = inst_module.bandwidth_ranges_and_unit

        applicable_obs_freq_instruments = []
        applicable_bandw_instruments = []

        # # Get float value of each parameter to be able to make comparison
        # obs_freq = float(obs_freq.value)
        # bandwidth = float(bandwidth.value)

        # Check what instrument/s the observing frequency value falls in
        for instrument, obs_freqs in instrument_obs_freqs.items():
            obs_freq_ranges = obs_freqs['ranges']
            for range in obs_freq_ranges:
                range = re.findall(r"[\d.]+", range)
                min_freq = float(range[0])
                max_freq = float(range[1])
                if obs_freq >= min_freq and obs_freq <= max_freq:
                    applicable_obs_freq_instruments.append(instrument)

        # Check what instrument/s the bandwidth value falls in
        for instrument, bandw_vals in instrument_bandw_vals.items():
            bandw_val_ranges = bandw_vals['ranges']
            for range in bandw_val_ranges:
                range = re.findall(r"[\d.]+", range)
                min_bandw = float(range[0])
                max_bandw = float(range[1])
                if bandwidth >= min_bandw and bandwidth <= max_bandw:
                    applicable_bandw_instruments.append(instrument)

        # Create a set of both applicable instruments lists and take the intersection
        applicable_instruments = list(set(applicable_obs_freq_instruments) & \
                                      set(applicable_bandw_instruments))
        # NOTE: Adding this sorting functionality to keep consistency until further
        # logic on how to choose an instrument if there are multiple applicable
        # instruments
        applicable_instruments = sorted(applicable_instruments)
        # If there are more than 1 applicable instrument
        if len(applicable_instruments) > 1:
            # TODO: there might be further logic incorporated to choose which instrument 
            # will be defaulted currently we are choosing the second applicable instrument
            chosen_inst_name = applicable_instruments[1]
        if len(applicable_instruments) == 1: # If there is only 1 applicable instrument
            chosen_inst_name = applicable_instruments[0]
        else: # If there is no applicable instrument
            chosen_inst_name = "Default"
        
        # Get the instrument module according to instrument name
        return inst_modules[chosen_inst_name]