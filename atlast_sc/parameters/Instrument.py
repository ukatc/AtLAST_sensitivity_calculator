from atlast_sc.utils import FileHelper

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
        self.data = FileHelper.read_instrument_file("gltcam")
        super().__init__(self.data)
        
    ################################################
    # Additional instrument specific methods below #
    ################################################

"""
TIFUUN instrument parameters
"""        
class Tifuun(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_file("tifuun")
        super().__init__(self.data)

    ################################################
    # Additional instrument specific methods below #
    ################################################

"""
MUSCAT instrument parameters
"""        
class Muscat(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_file("muscat")
        super().__init__(self.data)

    ################################################
    # Additional instrument specific methods below #
    ################################################

"""
FINER instrument parameters
"""        
class Finer(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_file("finer")
        super().__init__(self.data)

    ################################################
    # Additional instrument specific methods below #
    ################################################

"""
CHAI instrument parameters
"""        
class Chai(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_file("chai")
        super().__init__(self.data)

    ################################################
    # Additional instrument specific methods below #
    ################################################

"""
SEPIA345 instrument parameters
"""        
class Sepia345(Instrument):
    def __init__(self):
        self.data = FileHelper.read_instrument_file("sepia")
        super().__init__(self.data)

    ################################################
    # Additional instrument specific methods below #
    ################################################