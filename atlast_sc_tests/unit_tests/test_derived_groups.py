import pytest
import astropy.units as u
from atlast_sc.derived_groups import AtmosphereParams, Temperatures, \
    Efficiencies
from atlast_sc_tests.utils import create_default_inst_class, find_chosen_instrument

class TestAtmosphereParams:

    def test__init__(self):
        AtmosphereParams()
        # Nothing to test here
        assert True


class TestEfficiencies:

    def test__init__(self, obs_freq, surface_rms, eta_ill, eta_spill,
                     eta_block, eta_pol, mocker):

        calculate_eta_a_spy = \
            mocker.spy(Efficiencies,
                       '_calculate_eta_a')

        efficiencies = Efficiencies(obs_freq, surface_rms, eta_ill,
                                    eta_spill, eta_block, eta_pol)

        # Check that the dish efficiency has been calculated and the
        # value correctly mapped
        calculate_eta_a_spy.assert_called_once()
        expected_eta_a = \
            Efficiencies._calculate_eta_a(obs_freq, surface_rms, eta_ill,
                                          eta_spill, eta_block, eta_pol)
        assert expected_eta_a == efficiencies.eta_a


class TestTemperatures:

    def test__init__(self, obs_freq, bandwidth, weather, elevation, t_cmb, t_amb,
                     eta_eff, atmosphere_params, n_pol, mocker):

        transmittance = atmosphere_params.calculate_transmittance(obs_freq, weather,
                                                      elevation)
        T_atm = atmosphere_params.calculate_atmospheric_temperature(obs_freq,
                                                                    weather)
        
        chosen_inst = find_chosen_instrument(obs_freq, bandwidth)
        calculate_system_temp_spy = \
            mocker.spy(chosen_inst, 'calculate_system_temperature')
        
        temperatures = Temperatures(chosen_inst, obs_freq, bandwidth, t_cmb, t_amb, eta_eff, T_atm, 
                                    transmittance, n_pol)

        # Check that the receiver temperature has been calculated and the
        # value correctly mapped for Default instrument
        expected_receiver_temperature = 97.42463438933429 * u.K
        assert pytest.approx(expected_receiver_temperature.value) == chosen_inst.T_rx.value
        assert expected_receiver_temperature.unit == chosen_inst.T_rx.unit

        # Check that the system temperature has been calculated and the
        # value correctly mapped
        calculate_system_temp_spy.assert_called_once()

        expected_system_temperature = chosen_inst.T_sys
        assert expected_system_temperature == temperatures.T_sys
