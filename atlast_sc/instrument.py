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