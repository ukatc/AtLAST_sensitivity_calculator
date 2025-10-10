from atlast_sc.utils import FileHelper
import astropy.units as u
from atlast_sc.utils import Decorators
import functools

class Instrument():
    def __init__(self, data):
        self.data = data
        self.name = self.set_name(self.data)
        self.obs_freq_ranges_and_unit = self.set_obs_freq_ranges_and_unit(self.data)
        self.bandwidth_ranges_and_unit = self.set_bandwidth_ranges_and_unit(self.data)
        self.receiver_temp_options_and_unit = self.set_receiver_temp_options_and_unit(self.data)

    def set_name(self, data):
        """Set the name of the instrument."""
        return data.name

    def set_obs_freq_ranges_and_unit(self, data):
        return ( data.allowed_ranges["observing_frequency"]["ranges"], 
            data.allowed_ranges["observing_frequency"]["unit"] )
       
    def set_bandwidth_ranges_and_unit(self, data):
        return ( data.allowed_ranges["bandwidth"]["ranges"], 
            data.allowed_ranges["bandwidth"]["unit"])
    
    def set_receiver_temp_options_and_unit(self, data):
        return (data.receiver_temperature["values"],
            data.receiver_temperature["unit"])
   
"""
GLTCam instrument parameters
"""
class GLTCam(Instrument):

    def __init__(self):
        self.data = FileHelper.read_instrument_yaml_file("gltcam")
        super().__init__(self.data)
        self._T_rx = self._set_receiver_temp()

    ##################################
    # Instrument specific parameters #
    ##################################
        
    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    @staticmethod
    def _set_receiver_temp():
        return 22.0 * u.K
    
"""
TIFUUN instrument parameters
"""        
class Tifuun(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_yaml_file("tifuun")
        super().__init__(self.data)
        self._T_rx = self._set_receiver_temp()

    ##################################
    # Instrument specific parameters #
    ##################################
        
    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    @staticmethod
    def _set_receiver_temp():
        return 72.3 * u.K

"""
MUSCAT instrument parameters
"""        
class Muscat(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_yaml_file("muscat")
        super().__init__(self.data)
        self._T_rx = self._set_receiver_temp()
    
    ##################################
    # Instrument specific parameters #
    ##################################

    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    @staticmethod
    def _set_receiver_temp():
        return 44.7 * u.K

"""
FINER instrument parameters
"""        
class Finer(Instrument):
    def __init__(self, obs_freq):
        self.data = FileHelper.read_instrument_yaml_file("finer")
        super().__init__(self.data)
        self._T_rx = self._set_receiver_temp(obs_freq)

    ##################################
    # Instrument specific parameters #
    ##################################

    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    @staticmethod
    def _set_receiver_temp(obs_freq):
        # TODO: ASC-62 accessing the value of the object might
        # have to be done somewhere else
        obs_freq = obs_freq.value 
        if obs_freq >= 120.0 and obs_freq <= 210.0:
            return 45.0 * u.K
        elif obs_freq > 210.0 and obs_freq <= 360.0:
            return 75.0 * u.K

"""
CHAI instrument parameters
"""        
class Chai(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_yaml_file("chai")
        super().__init__(self.data)
        self._T_rx = self._set_receiver_temp()
        
    ##################################
    # Instrument specific parameters #
    ##################################

    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    @staticmethod
    def _set_receiver_temp():
        return 125.0 * u.K

"""
SEPIA345 instrument parameters
"""        
class Sepia345(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_yaml_file("sepia")
        super().__init__(self.data)
        self._T_rx = self._set_receiver_temp()

    ##################################
    # Instrument specific parameters #
    ##################################
        
    @property 
    def T_rx(self):
        return self._T_rx
    
    @T_rx.setter
    def T_rx(self, value):
        self._T_rx = value

    ################################################
    # Additional instrument specific methods below #
    ################################################

    @staticmethod
    def _set_receiver_temp():
        return 125.0 * u.K