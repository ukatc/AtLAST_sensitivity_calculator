import astropy.units as u

###########################################################
# Getters and setters for instrument specific parameters  #
###########################################################

class InstrumentSpecificParameters:
    
    # TODO:  temporary sideband ratio value to be used in
    # instrument modules. Note that the default value for 
    # this parameter is already 0. We are repeating this 
    # declaration here to pre-write instrument specific
    # g value retrieval. When further guidance is provided
    # on how each instrument will have individual sideband 
    # ratio values, the sideband ratio values in each 
    # instrument module will be changed accordingly.
    temporary_universal_g = 0

    def __init__(self):
        pass

    """
    DESHIMA instrument parameters
    """
    class GLTCam:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()
            self._name = "gltcam"

        @property
        def T_rx(self):
            "Get the receiver temperature of GLTCam instrument"
            return self._T_rx
        
        @property
        def g(self):
            "Get sideband ratio of GLTCam instrument"
            return InstrumentSpecificParameters.temporary_universal_g
        
        @property
        def name(self):
            "Get name of the instrument"
            return self._name

        @staticmethod
        def _set_receiver_temp():
            return 22.0 * u.K

    """
    TIFUUN instrument parameters
    """        
    class Tifuun:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()
            self._name = "tifuun"

        @property
        def T_rx(self):
            "Get the receiver temperature of TIFUUN instrument"
            return self._T_rx
        
        @property
        def g(self):
            "Get sideband ratio of TIFUUN instrument"
            return InstrumentSpecificParameters.temporary_universal_g
        
        @property
        def name(self):
            "Get name of the instrument"
            return self._name

        @staticmethod
        def _set_receiver_temp():
            return 72.3 * u.K
        
    """
    MUSCAT instrument parameters
    """          
    class Muscat:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()
            self._name = "muscat"

        @property
        def T_rx(self):
            "Get the receiver temperature of MUSCAT instrument"
            return self._T_rx
        
        @property
        def g(self):
            "Get sideband ratio of MUSCAT instrument"
            return InstrumentSpecificParameters.temporary_universal_g
        
        @property
        def name(self):
            "Get name of the instrument"
            return self._name

        @staticmethod
        def _set_receiver_temp():
            return 44.7 * u.K
        
    """
    FINER instrument parameters
    """        
    class Finer:
        def __init__(self, obs_freq):
            self._T_rx = self._set_receiver_temp(obs_freq)
            self._name = "finer"

        @property
        def T_rx(self):
            "Get the receiver temperature of FINER instrument"
            return self._T_rx
        
        @property
        def g(self):
            "Get sideband ratio of FINER instrument"
            return InstrumentSpecificParameters.temporary_universal_g
        
        @property
        def name(self):
            "Get name of the instrument"
            return self._name

        @staticmethod
        def _set_receiver_temp(obs_freq):
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
            self._name = "chai"

        @property
        def T_rx(self):
            "Get the receiver temperature of CHAI instrument"
            return self._T_rx

        @property
        def g(self):
            "Get sideband ratio of CHAI instrument"
            return InstrumentSpecificParameters.temporary_universal_g
        
        @property
        def name(self):
            "Get name of the instrument"
            return self._name
        
        @staticmethod
        def _set_receiver_temp():
            return 125.0 * u.K
        
    """
    SEPIA345 instrument parameters
    """     
    class Sepia345:
        def __init__(self):
            self._T_rx = self._set_receiver_temp()
            self._name = "sepia"

        @property
        def T_rx(self):
            "Get the receiver temperature of SEPIA345 instrument"
            return self._T_rx
        
        @property
        def g(self):
            "Get sideband ratio of SEPIA345 instrument"
            return InstrumentSpecificParameters.temporary_universal_g
        
        @property
        def name(self):
            "Get name of the instrument"
            return self._name

        @staticmethod
        def _set_receiver_temp():
            return 125.0 * u.K