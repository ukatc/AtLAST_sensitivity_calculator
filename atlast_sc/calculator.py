import warnings
import astropy.units as u
from astropy.constants import k_B
import numpy as np
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.models import DerivedParams
from atlast_sc.models import UserInput
from atlast_sc.config import Config
from atlast_sc.parameters.instrument_specific_parameters import InstrumentSpecificParameters
from atlast_sc.parameters.user_input_parameters import UserInputParameters
from atlast_sc.parameters.instrument_setup_parameters import InstrumentSetupParameters
from atlast_sc.parameters.telescope_and_environment_parameters import TelescopeAndEnvironmentParameters
from atlast_sc.parameters.derived_parameters import DerivedParameters
from atlast_sc.utils import DataHelper
from atlast_sc.exceptions import CalculatedValueInvalidWarning
from atlast_sc.exceptions import ValueOutOfRangeException


class Calculator:
    """
    Calculator class that provides an interface to the main
    calculator functionality and performs the core calculations
    to determine the output sensitivity or integration time.

    :param user_input: Dictionary containing user-defined input parameters
    :type user_input: dict
    :param instrument_setup: Dictionary containing instrument setup parameters.
     **NB: usage not tested, and may not be supported in future.**
    :type instrument_setup: dict
    """
    def __init__(self, user_input={}, instrument_setup={}, finetune=False):
        self._finetune = finetune


        # Make sure the user input doesn't contain any unexpected parameter
        # names
        Calculator._check_input_param_names(user_input)

        # Store the input parameters used to initialise the calculator
        self._config = Config(user_input, instrument_setup)

        # Calculate the derived parameters used in the calculation
        self._uip = UserInputParameters(self._config)
        self._isp = InstrumentSetupParameters(self._config)
        self._taep = TelescopeAndEnvironmentParameters(self._config)

        self.sensitivity = self._uip.sensitivity

        self._inst_name = self.find_applicable_instruments()

        derived_params =  self._calculate_derived_parameters(self._inst_name)
        self._dp = DerivedParameters(derived_params, self._config)

    #################################################
    # Public methods for performing sensitivity and #
    # integration time calculations                 #
    #################################################

    def calculate_sensitivity(self, t_int=None, update_calculator=True):
        """
        Calculates the telescope sensitivity (mJy) for a
        given integration time `t_int`.

        :param t_int: integration time. Optional. Defaults to the internally
            stored value
        :type t_int: astropy.units.Quantity
        :param update_calculator: True if the calculator should be updated with
            the specified integration time and calculated sensitivity.
            Optional. Defaults to True
        :type update_calculator: bool
        :return: sensitivity in mJy
        :rtype: astropy.units.Quantity
        """

        if t_int is not None:
            if update_calculator:
                self._uip.t_int = t_int
            else:
                DataHelper.validate(self, 't_int', t_int)
        else:
            t_int = self._uip.t_int

        sensitivity = \
            self._dp.sefd / \
            (self._dp.eta_s * np.sqrt(self._uip.n_pol * self._uip.bandwidth * t_int))

        # Convert the output to the most convenient units
        sensitivityresult = sensitivity.to(u.mJy)
        if  sensitivityresult < 1*u.mJy:
            sensitivity = sensitivity.to(u.uJy)
        elif (sensitivityresult >= 1*u.mJy) & (sensitivityresult < 1000*u.mJy):
            sensitivity = sensitivity.to(u.mJy)
        elif sensitivityresult >= 1000*u.mJy:
            sensitivity = sensitivity.to(u.Jy)

        # Try to update the sensitivity stored in the calculator
        if update_calculator:
            try:
                self.sensitivity = sensitivity
            except ValueOutOfRangeException as e:
                # This point is actually unreachable, but it's sensible to
                # have the code in place in case the permitted range of
                # the sensitivity changes and becomes possible to achieve with
                # the right combination of input parameters.
                message = \
                    Calculator._calculated_value_error_msg(sensitivity, e)
                warnings.warn(message, CalculatedValueInvalidWarning)

        return sensitivity

    def calculate_t_integration(self, sensitivity=None,
                                update_calculator=True):
        """
        Calculates the integration time required for a given `sensitivity`
        to be reached.

        :param sensitivity: required sensitivity. Optional. Defaults
            to the internally stored value
        :type sensitivity: astropy.units.Quantity
        :param update_calculator: True if the calculator should be updated with
            the specified sensitivity and calculated integration time.
            Optional. Defaults to True
        :type update_calculator: bool
        :return: integration time in seconds
        :rtype: astropy.units.Quantity
        """

        if sensitivity is not None:
            if update_calculator:
                self.sensitivity = sensitivity
            else:
                DataHelper.validate(self, 'sensitivity', sensitivity)
        else:
            sensitivity = self.sensitivity

        t_int = (self._dp.sefd / (sensitivity * self._dp.eta_s)) ** 2 \
            / (self._uip.n_pol * self._uip.bandwidth)

        # Convert the output to the most convenient units
        timeresult = t_int.to(u.s)
        if  timeresult < 60*u.s:
            t_int = t_int.to(u.s)
        elif (timeresult >= 60*u.s) & (timeresult < 3600*u.s):
            t_int = t_int.to(u.min)
        elif timeresult >= 3600*u.s:
            t_int = t_int.to(u.h)

        # Try to update the integration time stored in the calculator
        if update_calculator:
            try:
                self.t_int = t_int
            except ValueOutOfRangeException as e:
                message = Calculator._calculated_value_error_msg(t_int, e)
                warnings.warn(message, CalculatedValueInvalidWarning)

        return t_int

    ###################
    # Utility methods #
    ###################

    def reset(self):
        """
        Resets all calculator parameters to their initial values.
        """
        # Reset the config calculation inputs to their original values
        self._config.reset()
        # Recalculate the derived parameters
        self._calculate_derived_parameters()

    #####################
    # Protected methods #
    #####################

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

    def find_applicable_instruments(self):
        """
        Finds what instrument/s the observing frequency and bandwidth values
        inputted by the user correspond to and choose one to do the further
        calculations. 

        :return: applicable/chosen instrument name
        :rtype: String
        """
        # TODO: could make the finding applicable ranges more efficient by looking at general ranges first 

        # Instrument specific observing frequency ranges
        instrument_obs_freqs = {
            'finer' : [(120.0, 360.0)],
            'sepia' : [(163.0, 211.0), (272.0, 376.0), (600.0, 722.0)],
            'chai' : [(460.0, 500.0), (780.0, 820.0)],
            'tifuun' : [(90.0, 360.0)],
            'gltcam' : [(130.0, 170.0), (190.0, 250.0), (250.0, 295.0), (330.0, 365.0), (385.0, 415.0), (630.0, 710.0)],
            'muscat' : [(250.0, 300.0)]
        }

        # Instrument specific bandwidth value ranges
        instrument_bandw_vals = {
            'finer' : [(10500.0, 3000000.0)],
            'sepia' : [(10000.0, 5600000.0), (10000.0, 32000000.0), (10000.0, 10000000.0)],
            'chai' : [(10000.0, 1000000.0)],
            'tifuun' : [(10.0, 1000.0)],
            'gltcam' : [(1.0, 5.0)],
            'muscat' : [(1.0, 5.0)]
        }

        applicable_obs_freq_instruments = []
        applicable_bandw_instruments = []

        # Get float value of each parameter to be able to make comparison
        obs_freq = float(self._uip.obs_freq.value)
        bandwidth = float(self._uip.bandwidth.value)

        # Check what instrument/s the observing frequency value falls in
        for instrument, obs_freqs in instrument_obs_freqs.items(): 
            for tuple in obs_freqs:
                min_freq = tuple[0]
                max_freq = tuple[1]
                if obs_freq > min_freq and obs_freq < max_freq:
                    applicable_obs_freq_instruments.append(instrument)
        
        # Check what instrument/s the bandwidth value falls in
        for instrument, bandw_vals in instrument_bandw_vals.items():
            for tuple in bandw_vals:
                min_bandw = tuple[0]
                max_bandw = tuple[1]
                if bandwidth > min_bandw and bandwidth < max_bandw:
                    applicable_bandw_instruments.append(instrument)

        # Create a set of both applicable instruments lists and take the intersection
        applicable_instruments = list(set(applicable_obs_freq_instruments) & set(applicable_bandw_instruments))

        # If there are more than 1 applicable instrument
        if len(applicable_instruments) > 1:
            # TODO: there might be further logic incorporated to choose which instrument 
            # will be defaulted currently we are choosing the second applicable instrument
            return applicable_instruments[1]
        if len(applicable_instruments) == 1: # If there is only 1 applicable instrument
            return applicable_instruments[0]
        else: # If there is no applicable instrument
            # TODO: there might be further logic incorporated to choose which instrument 
            # will be chosen if there is no applicable instrument.
            # Currently we are choosing the closest instrument according to observing
            # frequencies.
            return self.closest_range_from_dict(obs_freq, instrument_obs_freqs)

    def closest_range_from_dict(self, obs_freq, range_dict):
        """
        Finds the closest range to a number from a dictionary of observing 
        frequency range lists, only if the number is not inside any of them.

        :param obs_freq: observing frequency
        :type obs_freq: float

        :return: closest instrument name
        :rtype: String or None if obs_freq is inside any range
        """

        # Find the closest range by distance to the nearest bound
        closest_inst = None
        min_distance = float('inf')

        for key, ranges in range_dict.items():
            for r in ranges:
                distance = min(abs(obs_freq - r[0]), abs(obs_freq - r[1]))
                if distance < min_distance:
                    min_distance = distance
                    closest_inst = key
        
        return closest_inst

    def _calculate_derived_parameters(self, inst_name):
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

        # Get instrument specific parameters object
        inst_spec_module = self._get_inst_spec_params_module(inst_name, self._uip.obs_freq)

        # Perform efficiencies calculations
        eta = Efficiencies(self._uip.obs_freq , self._taep.surface_rms, self._taep.eta_ill,
                           self._taep.eta_spill, self._taep.eta_block, self._isp.eta_pol)

        # Perform atmospheric model calculations
        atm = AtmosphereParams()
        tau_atm = atm.calculate_tau_atm(self._uip.obs_freq,
                                        self._uip.weather, self._uip.elevation)
        T_atm = atm.calculate_atmospheric_temperature(self._uip.obs_freq,
                                                      self._uip.weather)

        # Calculate the temperatures
        temps = Temperatures(inst_spec_module, self._uip.obs_freq, self._taep.T_cmb, self._taep.T_amb, inst_spec_module.g,
                             self._taep.eta_eff, T_atm, tau_atm)

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
        obs_freq_low = (self._uip.obs_freq-0.50*self._uip.bandwidth).to('GHz').value
        obs_freq_upp = (self._uip.obs_freq+0.50*self._uip.bandwidth).to('GHz').value

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
        if self._finetune and len(obs_freq_list)>1:
            
            _sefd = []
            
            obs_band_list = (obs_freq_list[1:]-obs_freq_list[:-1])
            obs_freq_list = (obs_freq_list[1:]+obs_freq_list[:-1])*0.50

            # compute SEFD for each narrow spectral element
            for freq in obs_freq_list:
                _tau_atm = atm.calculate_tau_atm(freq,self._uip.weather,self._uip.elevation)

                _T_atm = atm.calculate_atmospheric_temperature(freq,self._uip.weather)
                _temps = Temperatures(inst_spec_module, freq, self._taep.T_cmb, self._taep.T_amb, inst_spec_module.g,
                                      self._isp.eta_eff, _T_atm, _tau_atm)

                _sefd.append(self._calculate_sefd(_temps.T_sys,eta.eta_a).to('J/m2').value)
            _sefd = np.asarray(_sefd)*(u.J/u.m**2)

            # obtain the effective SEFD for the input band
            sefd = np.sqrt(self._uip.bandwidth/np.sum(obs_band_list/_sefd**2))
        else:
            sefd = self._calculate_sefd(temps.T_sys, eta.eta_a)

        _derived_params = \
            DerivedParams(tau_atm=tau_atm, T_atm=T_atm, T_rx=temps.T_rx,
                          eta_a=eta.eta_a, eta_s=eta.eta_s, T_sys=temps.T_sys, T_sky=temps.T_sky,
                          sefd=sefd)
        
        return _derived_params
    
    @staticmethod
    def _get_inst_spec_params_module(inst_name, obs_freq):
        """
        Returns the instrument module according to instrument 
        name and observing frequency value supplied. 

        TODO: Currently uses observing frequency in only one 
        instrument module according to guidelines provided by
        instrument teams. Observing frequency will be used in
        other instrument modules when guidelines are clearer.

        :param inst_name: instrument name
        :type inst_name: String
        :param obs_freq: observing frequency
        :type obs_freq: float
        :return: instrument module
        :rtype: atlast_sc.parameters.instrument_specific_parameters.InstrumentSpecificParameters
        """
        if inst_name is not None:
            match inst_name:
                case "deshima":
                    return InstrumentSpecificParameters.Deshima()
                   
                case "tifuun":
                    return InstrumentSpecificParameters.Tifuun()
                    
                case "muscat":
                    return InstrumentSpecificParameters.Muscat()
                    
                case "finer":
                    return InstrumentSpecificParameters.Finer(obs_freq)
                   
                case "chai":
                    return InstrumentSpecificParameters.Chai()
                    
                case "sepia":
                    return InstrumentSpecificParameters.Sepia345()

    def _calculate_sefd(self, T_sys, eta_a):
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

        dish_area = np.pi * self._taep.dish_radius ** 2
        sefd = (2 * k_B * T_sys) / (eta_a * dish_area)

        return sefd

    @staticmethod
    def _calculated_value_error_msg(calculated_value, validation_error):
        """
        The message displayed when a calculated value (t_int or sensitivity) is
        outside the permitted range.

        :param calculated_value: the calculated value of the target parameter
        :type calculated_value: astropy.units.Quantity
        :param validation_error: the error raised when validating the
            calculated parameter value
        :type validation_error: atlast_sc.exceptions.ValueOutOfRangeException
        """

        message = f"The calculated value {calculated_value.round(4)} " \
                  f"is outside of the permitted range " \
                  f"for parameter '{validation_error.parameter}'. " \
                  f"{validation_error.message} " \
                  f"The Calculator will not be updated with the new value. " \
                  f"Please adjust the input parameters and recalculate."

        return message

