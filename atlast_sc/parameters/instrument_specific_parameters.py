import astropy.units as u

###########################################################
# Getters and setters for instrument specific parameters  #
###########################################################

class InstrumentSpecificParameters:
    def __init__(self, instrument_name):
        self.instrument_name = instrument_name

    """
    DESHIMA instrument parameters
    """
    class Deshima:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()

        @property
        def T_rx(self):
            "Get the receiver temperature of DESHIMA instrument"
            return self._T_rx

        @staticmethod
        def _set_receiver_temp():
            return 22.0 * u.K

    """
    TIFUUN instrument parameters
    """        
    class Tifuun:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()

        @property
        def T_rx(self):
            "Get the receiver temperature of TIFUUN instrument"
            return self._T_rx

        @staticmethod
        def _set_receiver_temp():
            return 72.3 * u.K
        
    """
    MUSCAT instrument parameters
    """          
    class Muscat:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()

        @property
        def T_rx(self):
            "Get the receiver temperature of MUSCAT instrument"
            return self._T_rx

        @staticmethod
        def _set_receiver_temp():
            return 44.7 * u.K
        
    """
    FINER instrument parameters
    """        
    class Finer:
        def __init__(self, obs_freq):
            self._T_rx = self._set_receiver_temp(obs_freq)

        @property
        def T_rx(self):
            "Get the receiver temperature of FINER instrument"
            return self._T_rx

        @staticmethod
        def _set_receiver_temp(obs_freq):
            obs_freq = obs_freq.value # needed to compare double vals
            if obs_freq > 120.0 and obs_freq < 210.0:
                return 45.0 * u.K
            elif obs_freq > 210.0 and obs_freq < 360.0:
                return 75.0 * u.K
            
    """
    CHAI instrument parameters
    """     
    class Chai:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()

        @property
        def T_rx(self):
            "Get the receiver temperature of CHAI instrument"
            return self._T_rx

        @staticmethod
        def _set_receiver_temp():
            return 125.0 * u.K
        
    """
    SEPIA345 instrument parameters
    """     
    class Sepia345:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()

        @property
        def T_rx(self):
            "Get the receiver temperature of SEPIA345 instrument"
            return self._T_rx

        @staticmethod
        def _set_receiver_temp():
            return 125.0 * u.K