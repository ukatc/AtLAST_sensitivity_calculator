import astropy.units as u
from astropy import constants
from atlast_sc.data import Validator, Data

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
        # Validate the unit specified in instrument files
        Validator.validate_units(data.allowed_ranges["observing_frequency"]["unit"],
                                 'obs_freq', Data.obs_frequency)
    
        return ( {'ranges': data.allowed_ranges["observing_frequency"]["ranges"],
                  'unit': data.allowed_ranges["observing_frequency"]["unit"]} )
       
    def set_bandwidth_ranges_and_unit(self, data):
        # Validate the unit specified in instrument files
        Validator.validate_units(data.allowed_ranges["bandwidth"]["unit"],
                                 'bandwidth', Data.bandwidth)
        
        return ( {'ranges': data.allowed_ranges["bandwidth"]["ranges"],
                  'unit': data.allowed_ranges["bandwidth"]["unit"]} )
    
    def set_receiver_temp_options_and_unit(self, data):
        # ASC-76 Currently not validating receiver temp units because 
        # values provided directly in the instrument files are temporary.
        return ( {'values': data.receiver_temperature["values"],
                  'unit': data.receiver_temperature["unit"]} )
    
    #####################################
    # Instrument class specific methods #
    #####################################

# ATLAST instruments 
   
"""
GLTCam instrument parameters
"""
class GLTCam(Instrument):

    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp()

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

    def calculate_receiver_temp(self, obs_freq):
        # NOTE: This will be populated with instrument specific 
        # receiver temperature calculation equation.
        temp = 22.0 * u.K
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp():
        return 22.0 * u.K
    
"""
TIFUUN instrument parameters
"""        
class Tifuun(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp()

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

    def calculate_receiver_temp(self, obs_freq):
        # NOTE: This will be populated with instrument specific 
        # receiver temperature calculation equation.
        temp = 72.3 * u.K
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp():
        return 72.3 * u.K

"""
MUSCAT instrument parameters
"""        
class Muscat(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp()
    
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

    def calculate_receiver_temp(self, obs_freq):
        # NOTE: This will be populated with instrument specific 
        # receiver temperature calculation equation.
        temp = 44.7 * u.K
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp():
        return 44.7 * u.K

"""
FINER instrument parameters
"""        
class Finer(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp()

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

    def calculate_receiver_temp(self, obs_freq):
        obs_freq = obs_freq.value 
        if obs_freq >= 120.0 and obs_freq <= 210.0:
            temp = 45.0 * u.K
        elif obs_freq > 210.0 and obs_freq <= 360.0:
            temp = 75.0 * u.K
        self.T_rx = temp
        return temp
        
    @staticmethod
    def _set_default_receiver_temp():
        return 45.0 * u.K

"""
CHAI instrument parameters
"""        
class Chai(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp(self.receiver_temp_options_and_unit)
        
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

    def calculate_receiver_temp(self, obs_freq):
        # NOTE: This will be populated with instrument specific 
        # receiver temperature calculation equation.
        temp = 125.0 * u.K
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp(receiver_temp_options_and_unit):
        receiver_temp = u.Quantity(receiver_temp_options_and_unit['values'][0],
                                    u.K)
        return receiver_temp

"""
SEPIA345 instrument parameters
"""        
class Sepia345(Instrument):
    def __init__(self, data):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp()

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

    def calculate_receiver_temp(self, obs_freq):
        # NOTE: This will be populated with instrument specific 
        # receiver temperature calculation equation.
        temp = 125.0 * u.K
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp():
        return 125.0 * u.K
    
"""
Default instrument parameters
"""        
class Default(Instrument):
    def __init__(self, data, obs_freq):
        super().__init__(data)
        self._T_rx = self._set_default_receiver_temp(obs_freq)

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

    def calculate_receiver_temp(self, obs_freq):
        temp = (5 * constants.h * obs_freq / constants.k_B).to(u.K)
        self.T_rx = temp
        return temp

    @staticmethod
    def _set_default_receiver_temp(obs_freq):
        return (5 * constants.h * obs_freq / constants.k_B).to(u.K)