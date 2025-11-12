import copy, re
from atlast_sc.models import UserInput
from atlast_sc.models import InstrumentSpecific
from atlast_sc.models import CalculationInput
from atlast_sc.models import CalculationResult
from atlast_sc.models import TelescopeAndEnvironment

from atlast_sc.instruments.config import InstrumentConfig

from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.models import DerivedParams

import astropy.units as u
from astropy.constants import k_B
import numpy as np

class ParameterSetup:
    """
    Class that holds the user input and instrument setup parameters
    used to perform the sensitivity calculations.
    """
    def __init__(self, user_input={}, instrument_specific={}, telescope_and_environment={}, finetune=False):
        """
        Initialises all the required parameters from user_input and
        instrument_specific.

        :param user_input: A dictionary of user inputs of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type user_input: dict
        :param instrument_specific: A dictionary of instrument setup parameters
        of structure
        {'param_name':{'value': <value>, 'unit': <unit>}}
        :type instrument_specific: dict
        """

        # Make sure the user input doesn't contain any unexpected parameter names
        self._check_input_param_names(user_input)

        self.finetune = finetune

        # Parameters
        new_user_input = UserInput(**user_input)
        new_instrument_specific = InstrumentSpecific(**instrument_specific)
        new_telescope_and_environment = TelescopeAndEnvironment(**telescope_and_environment)

        self._calculation_inputs = \
            CalculationInput(user_input=new_user_input,
                             instrument_specific=new_instrument_specific,
                             telescope_and_environment=new_telescope_and_environment)
        
        self._calculation_results = CalculationResult()

        # Get instrument config 
        inst_config = InstrumentConfig()
        # Get loaded instrument classes
        self.loaded_instruments = inst_config.instrument_classes
        
        self._derived_parameters_model = self._calculate_derived_parameters()
        
        # Make a deep copy of the calculation inputs to enable the
        # calculator to be reset to its initial setup
        self._original_inputs = copy.deepcopy(self._calculation_inputs)


    @property
    def calculation_inputs(self):
        """
        The inputs to the calculation (user input and instrument setup)
        """
        return self._calculation_inputs
    
    @property
    def calculation_results(self):
        """
        Calculated integration time and sensitivity variables
        """
        return self._calculation_results

    @property
    def user_input(self):
        """
        User inputs to the calculation
        """
        return self._calculation_inputs.user_input
  
    @property
    def instrument_specific(self):
        """
        Instrument specific parameters
        """
        return self._calculation_inputs.instrument_specific
    
    @property
    def telescope_and_environment(self):
        """
        Telescope and environment parameters
        """
        return self._calculation_inputs.telescope_and_environment
      
    @property
    def derived_parameters_model(self):
        """
        Get derived parameters calculated from user input and instrument specific parameters
        """
        return self._derived_parameters_model
    
    @derived_parameters_model.setter
    def derived_parameters_model(self, new_model):
        """
        Set derived parameters calculated from user input and instrument specific parameters
        """
        self._derived_parameters = new_model

    def reset(self):
        """
        Resets the calculator configuration parameters (user input and
        instrument setup to their original values.
        """
        self._calculation_inputs = \
            self._original_inputs
        
    @staticmethod
    def _check_input_param_names(user_input):
        """
        Validates the user input parameters (just the names; value validation
        is handled by the model)

        :param user_input: Dictionary containing user-defined input parameters
        :type user_input: dict
        """

        test_model = UserInput()

        for param in user_input:
            if param not in test_model.__dict__:
                raise ValueError(f'"{param}" is not a valid input parameter')
            
    def get_chosen_instrument(self):
        """
        (ASC-76)
        Retrieve the instrument object class according to observing frequency
        and bandwidth values the user has provided. 

        :return: instrument module
        :rtype: atlast_sc.parameters.Instrument
        """
        # Look at obs_freq and bandwidth values
        user_obs_freq = self.user_input.obs_freq.value
        user_bandwidth = self.user_input.bandwidth.value
        # See which instrument those values correspond to
        chosen_inst_name = self.find_applicable_instruments(obs_freq=user_obs_freq, bandwidth=user_bandwidth)
        # Get the instrument module according to instrument name
        chosen_inst = self.loaded_instruments[chosen_inst_name]
        return chosen_inst

    def find_applicable_instruments(self, obs_freq, bandwidth):
        """
        Finds what instrument/s the observing frequency and bandwidth values
        inputted by the user correspond to and choose one to do the further
        calculations. 

        :return: applicable/chosen instrument name
        :rtype: String
        """
        # TODO: could make the finding applicable ranges more efficient by looking at general ranges first 

        instrument_obs_freqs = {} # Instrument specific observing frequency ranges
        instrument_bandw_vals = {} # Instrument specific bandwidth value ranges
        for inst_name, inst_module in self.loaded_instruments.items():
            instrument_obs_freqs[inst_name] = inst_module.obs_freq_ranges_and_unit
            instrument_bandw_vals[inst_name] = inst_module.bandwidth_ranges_and_unit

        applicable_obs_freq_instruments = []
        applicable_bandw_instruments = []

        # Get float value of each parameter to be able to make comparison
        obs_freq = float(obs_freq.value)
        bandwidth = float(bandwidth.value)

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
            return applicable_instruments[1]
        if len(applicable_instruments) == 1: # If there is only 1 applicable instrument
            return applicable_instruments[0]
        else: # If there is no applicable instrument
            return "Default"
        
    def _calculate_derived_parameters(self):
        """
        Performs the calculations required to produce the
        set of derived parameters required for the sensitivity
        calculation.
        """
        # TODO Technically, it's possible to instantiate each of the
        # classes below using a different observing frequency for each.
        # The resulting derived parameters wouldn't make sense under those
        # circumstances. Although this is an unlikely scenario, the design
        # would be cleaner if there three classes referenced the
        # same observing frequency.
        # Implement a Builder interface to construct all three objects using
        # the same observing frequency?

        # LDM
        # ------------------------------------------------------------------
        # T_atm, tau_atm, and the various temps values are not actually used
        # for computing the sefd, but I kept this part to avoid breaking the
        # build of DerivedParams below
        # ------------------------------------------------------------------
        obs_freq = self.calculation_inputs.user_input.obs_freq.value
        weather = self.calculation_inputs.user_input.weather.value
        elevation = self.calculation_inputs.user_input.elevation.value
        bandwidth = self.calculation_inputs.user_input.bandwidth.value
        surface_rms = self.calculation_inputs.telescope_and_environment.surface_rms.value
        dish_radius = self.calculation_inputs.telescope_and_environment.dish_radius.value
        eta_eff = self.calculation_inputs.telescope_and_environment.eta_eff.value
        eta_ill= self.calculation_inputs.telescope_and_environment.eta_ill.value
        eta_spill= self.calculation_inputs.telescope_and_environment.eta_spill.value
        eta_block = self.calculation_inputs.telescope_and_environment.eta_block.value
        T_cmb = self.calculation_inputs.telescope_and_environment.T_cmb.value
        T_amb = self.calculation_inputs.telescope_and_environment.T_amb.value
        eta_pol = self.calculation_inputs.instrument_specific.eta_pol.value
        g = self.calculation_inputs.instrument_specific.g.value

        # Get chosen instrument and its receiver temperature
        # chosen_inst = self.chosen_inst
        chosen_inst = self.get_chosen_instrument()
        inst_spec_T_rx = chosen_inst.calculate_receiver_temp(obs_freq=obs_freq)

        # Perform efficiencies calculations
        eta = Efficiencies(obs_freq , surface_rms, eta_ill,
                            eta_spill, eta_block, eta_pol)

        # Perform atmospheric model calculations
        atm = AtmosphereParams()
        tau_atm = atm.calculate_tau_atm(obs_freq,
                                        weather, elevation)
        T_atm = atm.calculate_atmospheric_temperature(obs_freq,
                                                        weather)
        # Calculate the temperatures
        temps = Temperatures(obs_freq, T_cmb, T_amb, g,
                                eta_eff, T_atm, tau_atm, inst_spec_T_rx)

        # LDM
        # ------------------------------------------------------------------
        # This is where the snippet starts. The idea is to compute an
        # effect SEFD as sefd_eff = sqrt(dnu/sum(dnu_i/sefd_i)), where dnu
        # is the total bandwidth and dnu_i the widths of the narrow channels
        # for which we compute each sefd_i. This comes from basic noise 
        # statistics consideration for computing the total RMS for a broad
        # band composed of n independent channels. 
        # Setting finetune=False will fall back on the old implementation
        # ------------------------------------------------------------------

        # define lower and upper limit of the requested band
        obs_freq_low = (obs_freq-0.50*bandwidth).to('GHz').value
        obs_freq_upp = (obs_freq+0.50*bandwidth).to('GHz').value
        # select all the frequencies in the atm tables comprised within the band edges
        obs_freq_list = atm.tau_atm_table[:, 0][np.logical_and(atm.tau_atm_table[:, 0]>obs_freq_low,
                                                                atm.tau_atm_table[:, 0]<obs_freq_upp)]

        # pad the frequency array to include the lower/upper band edges 
        obs_freq_list = np.concatenate(([obs_freq_low],obs_freq_list,[obs_freq_upp]))*u.GHz

        # double the frequency resolution; turned off for the moment, but
        # just wanted to keep track of this
        # if False:
        #     obs_freq_list = np.ravel([obs_freq_list[1:],0.50*(obs_freq_list[1:]+obs_freq_list[:-1])],'F')
        #     obs_freq_list = np.append(obs_freq_low,obs_freq_list)

        # check if there are enough channels for performing the sum,
        # otherwise estimate the single-frequency SEFD
        if self.finetune and len(obs_freq_list)>1:
            _sefd = []

            obs_band_list = (obs_freq_list[1:]-obs_freq_list[:-1])
            obs_freq_list = (obs_freq_list[1:]+obs_freq_list[:-1])*0.50

            # compute SEFD for each narrow spectral element
            for freq in obs_freq_list:
                _tau_atm = atm.calculate_tau_atm(freq,weather,elevation)

                _T_atm = atm.calculate_atmospheric_temperature(freq,weather)
                _temps = Temperatures(freq, T_cmb, T_amb, g,
                                        eta_eff, _T_atm, _tau_atm)

                _sefd.append(self._calculate_sefd(_temps.T_sys,eta.eta_a, dish_radius).to('J/m2').value)
            _sefd = np.asarray(_sefd)*(u.J/u.m**2)

            # obtain the effective SEFD for the input band
            sefd = np.sqrt(bandwidth/np.sum(obs_band_list/_sefd**2))
        else:
            sefd = self._calculate_sefd(temps.T_sys, eta.eta_a, dish_radius)

        self._derived_parameters_model = \
            DerivedParams(tau_atm=tau_atm, T_atm=T_atm, T_rx=temps.T_rx,
                            eta_a=eta.eta_a, eta_s=eta.eta_s, T_sys=temps.T_sys, T_sky=temps.T_sky,
                            sefd=sefd)

        return self._derived_parameters_model
    
    def _calculate_sefd(self, T_sys, eta_a, dish_radius):
        """
        Calculates the source equivalent flux density, SEFD, from the system
        temperature, T_sys, the dish efficiency eta_A, and the dish area.
        :param T_sys: system temperature
        :type T_sys: astropy.units.Quantity
        :param eta_a: the dish efficiency factor
        :type eta_a: float
        :return: source equivalent flux density
        :rtype: astropy.units.Quantity
        """

        dish_area = np.pi * dish_radius ** 2
        sefd = (2 * k_B * T_sys) / (eta_a * dish_area)

        return sefd