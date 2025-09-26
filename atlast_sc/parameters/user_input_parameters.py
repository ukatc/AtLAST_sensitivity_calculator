from atlast_sc.utils import Decorators
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Temperatures
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.models import DerivedParams
from atlast_sc.parameters.derived_parameters import DerivedParameters
import astropy.units as u
from astropy.constants import k_B
import numpy as np

###################################################
# Getters and setters for user input parameters   #
###################################################

class UserInputParameters:

    def __init__(self, param_setup):
        self._param_setup = param_setup
        # Note: We are calculating and storing the derived parameters in this class
        # as they will be recalculated according to new user input.
        self._derived_parameters_model = self._calculate_derived_parameters() 
        self._derived_parameters = DerivedParameters(self._derived_parameters_model)

    # TODO t_int and sensitivity are a special can se. They can be both
    #   set and calculated. Special care needs to be taken on setting them:
    #   they will have to be validated if they're set, but not calculated.
    #   Also, if they're set, the user needs to be warned if they then try
    #   to use Calculator values with redoing the senstivity/integration time
    #   calculation
    @property
    def t_int(self):
        """
        Get or set the integration time
        """
        return self._param_setup.calculation_inputs.user_input.t_int.value

    @t_int.setter
    @Decorators.validate_value
    def t_int(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        # TODO: We don't technically need to update the unit here (ditto other
        #   values with units, because the value is set to a Quantity, which
        #   contains the units. It's this value that is used throughout the
        #   the application. However, not updating it feels odd, since it would
        #   result in a discrepancy between the unit property and the unit
        #   contained in the Quantity object. Think about this...
        self._param_setup.calculation_inputs.user_input.t_int.value = value
        self._param_setup.calculation_inputs.user_input.t_int.unit = value.unit

    @property
    def sensitivity(self):
        """
        Get or set the sensitivity
        """
        return self._param_setup.calculation_inputs.user_input.sensitivity.value

    @sensitivity.setter
    @Decorators.validate_value
    def sensitivity(self, value):
        # TODO: Setting this value in the on the inputs feels wrong.
        #  This may be a calculated param. Allowing the user to change it
        #  without restriction may lead to inaccurate output if they perform
        #  the sensitivity calculation, change the integration time, then
        #  store or use those stored values.
        #  Need separate "outputs" properties that are used for
        #  subsequent calculations and/or storing results?
        self._param_setup.calculation_inputs.user_input.sensitivity.value = value
        self._param_setup.calculation_inputs.user_input.sensitivity.unit = value.unit

    @property
    def bandwidth(self):
        """
        Get or set the bandwidth
        """
        return self._param_setup.calculation_inputs.user_input.bandwidth.value
    # With the new calculation of SEFD over the whole frequency range, SEFD is now dependent on bandwidth and so parameters must be updated every time bandwidth is changed.
    @bandwidth.setter
    @Decorators.validate_and_update_params
    def bandwidth(self, value):
        self._param_setup.calculation_inputs.user_input.bandwidth.value = value
        self._param_setup.calculation_inputs.user_input.bandwidth.unit = value.unit

    @property
    def obs_freq(self):
        """
        Get or set the sky frequency of the observations
        """
        return self._param_setup.calculation_inputs.user_input.obs_freq.value

    @obs_freq.setter
    @Decorators.validate_and_update_params
    def obs_freq(self, value):
        self._param_setup.calculation_inputs.user_input.obs_freq.value = value
        self._param_setup.calculation_inputs.user_input.obs_freq.unit = value.unit

    @property
    def n_pol(self):
        """
        Get or set the number of polarisations being observed
        """
        return self._param_setup.calculation_inputs.user_input.n_pol.value

    @n_pol.setter
    @Decorators.validate_value
    def n_pol(self, value):
        self._param_setup.calculation_inputs.user_input.n_pol.value = value

    @property
    def weather(self):
        """
        Get or set the relative humidity
        """
        return self._param_setup.calculation_inputs.user_input.weather.value

    @weather.setter
    @Decorators.validate_and_update_params
    def weather(self, value):
        self._param_setup.calculation_inputs.user_input.weather.value = value

    @property
    def elevation(self):
        """
        Get or set the elevation of the target for calculating air mass
        """
        return self._param_setup.calculation_inputs.user_input.elevation.value

    @elevation.setter
    @Decorators.validate_and_update_params
    def elevation(self, value):
        self._param_setup.calculation_inputs.user_input.elevation.value = value
        self._param_setup.calculation_inputs.user_input.elevation.unit = value.unit

    @property
    def derived_parameters(self):
        """
        Parameters calculated from user input and instrument specific
        """
        return self._derived_parameters

    @derived_parameters.setter
    def derived_parameters(self, value):
        self._derived_parameters = value

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

        obs_freq = self._param_setup.calculation_inputs.user_input.obs_freq.value
        weather = self._param_setup.calculation_inputs.user_input.weather.value
        elevation = self._param_setup.calculation_inputs.user_input.elevation.value
        bandwidth = self._param_setup.calculation_inputs.user_input.bandwidth.value
        surface_rms = self._param_setup.calculation_inputs.telescope_and_environment.surface_rms.value
        dish_radius = self._param_setup.calculation_inputs.telescope_and_environment.dish_radius.value
        eta_eff = self._param_setup.calculation_inputs.telescope_and_environment.eta_eff.value
        eta_ill= self._param_setup.calculation_inputs.telescope_and_environment.eta_ill.value
        eta_spill= self._param_setup.calculation_inputs.telescope_and_environment.eta_spill.value
        eta_block = self._param_setup.calculation_inputs.telescope_and_environment.eta_block.value
        T_cmb = self._param_setup.calculation_inputs.telescope_and_environment.T_cmb.value
        T_amb = self._param_setup.calculation_inputs.telescope_and_environment.T_amb.value
        eta_pol = self._param_setup.calculation_inputs.instrument_specific.eta_pol.value
        g = self._param_setup.calculation_inputs.instrument_specific.g.value

        chosen_inst = self._param_setup.get_chosen_instrument()
        inst_spec_T_rx = chosen_inst.T_rx
 
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
                                eta_eff, T_atm, tau_atm)

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
        if self._param_setup.finetune and len(obs_freq_list)>1:
            
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
            DerivedParams(tau_atm=tau_atm, T_atm=T_atm, T_rx=inst_spec_T_rx,
                            eta_a=eta.eta_a, eta_s=eta.eta_s, T_sys=temps.T_sys, T_sky=temps.T_sky,
                            sefd=sefd)

        # Update the copy of derived derived parameters within UserInputParameters class 
        # whether it's the first time calculating these parameters from default values
        # or if it's being re-calculated due to change in parameters.
        # NOTE and TODO: this is currently very hacky!! in initial execution of the method 
        # _calculate_derived_parameters, the self._derived_parameters variable does not
        # exist. So technically this line fails. But we still need it here for when 
        # _calculate_derived_parameters is executed during re-calculation of derived
        # parameters.
        self.derived_parameters = DerivedParameters(self._derived_parameters_model) 
        
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
    
    def show(self):
        for name in dir(self.__class__):
            if name == "derived_parameters": # Don't show derived_parameters
                continue
            attr = getattr(self.__class__, name)
            if isinstance(attr, property):
                value = getattr(self, name)
                print(f"{name}: {value}")