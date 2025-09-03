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
        self.gltcamdata = FileHelper.read_instrument_file("gltcam")
        super().__init__(self.gltcamdata)
        
    ################################################
    # Additional instrument specific methods below #
    ################################################