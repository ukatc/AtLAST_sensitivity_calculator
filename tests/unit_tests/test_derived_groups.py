from scipy.stats import linregress
import numpy as np
import pytest
import astropy.units as u
from astropy import constants
from atlast_sc.derived_groups import AtmosphereParams
from atlast_sc.derived_groups import Efficiencies
from atlast_sc.derived_groups import Temperatures

test_obs_frequency_bands = [
    (35, "band 1"),
    (60, "opaque"),
    (125, "band 3"),
    (150, "band 4"),
    (200, "band 5"),
    (250, "band 6"),
    (350, "band 7"),
    (380, "opaque"),
    (420, "band 8"),
    (550, "opaque"),
    (650, "band 9"),
    (750, "opaque"),
    (850, "band 10"),
]


class TestAtmosphereParams:

    @pytest.mark.parametrize('obs_freq,band', test_obs_frequency_bands)
    def test_calculate_tau_atm(self, obs_freq, band, weather,
                               atmosphere_params):

        elevations = [5, 45]

        tau_factors = []
        obs_freq = obs_freq * u.GHz
        for elevation in elevations:
            elevation = elevation * u.deg
            tau_factors.append(
                atmosphere_params.calculate_tau_atm(obs_freq, weather,
                                                    elevation)
            )

        # Check that the tau factor for the lower elevation is greater than the
        #   tau factor for the higher elevation
        assert tau_factors[0] > tau_factors[1]

        # Check that the tau factor is "high" for frequencies between bands
        for tau_factor in tau_factors:
            if band == "opaque":
                assert tau_factor > 10
            else:
                assert tau_factor < 10

    @pytest.mark.parametrize('obs_freq,band', test_obs_frequency_bands)
    def test__calculate_temperature(self, obs_freq, band, weather, elevation,
                                    atmosphere_params):

        obs_freq = obs_freq * u.GHz

        temp = atmosphere_params.calculate_atmospheric_temperature(obs_freq,
                                                                   weather)

        # Check that the atmospheric temperature is "cold" for transparent
        # frequencies and "hot" for opaque frequencies
        if band == "opaque":
            assert temp > 250 * u.K
        else:
            assert temp < 150 * u.K


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

    def test__calculate_eta_a(self, surface_rms, eta_ill, eta_spill,
                              eta_block, eta_pol):
        test_obs_freqs = \
            [35, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

        eta_As = []
        for obs_freq in test_obs_freqs:
            obs_freq = obs_freq * u.GHz

            eta_a = \
                Efficiencies._calculate_eta_a(obs_freq, surface_rms, eta_ill,
                                              eta_spill, eta_block, eta_pol)

            eta_As.append(eta_a)

        # Check that the dish efficiency, eta_a, decreases with increasing
        # observing frequency
        comparisons = [(x - eta_As[i - 1]) < 0
                       for i, x in enumerate(eta_As)][1:]
        assert all(comparisons)


class TestTemperatures:

    def test__init__(self, obs_freq, weather, elevation, t_cmb, t_amb, g,
                     eta_eff, atmosphere_params, mocker):

        calculate_receiver_temp_spy = \
            mocker.spy(Temperatures,
                       '_calculate_receiver_temperature')
        calculate_system_temp_spy = \
            mocker.spy(Temperatures, '_calculate_system_temperature')

        tau_atm = atmosphere_params.calculate_tau_atm(obs_freq, weather,
                                                      elevation)
        T_atm = atmosphere_params.calculate_atmospheric_temperature(obs_freq,
                                                                    weather)
        temperatures = Temperatures(obs_freq, t_cmb, t_amb, g,
                                    eta_eff, T_atm, tau_atm)

        # Check that the receiver temperature has been calculated and the
        # value correctly mapped
        calculate_receiver_temp_spy.assert_called_once()
        expected_receiver_temperature = \
            Temperatures._calculate_receiver_temperature(obs_freq)
        assert expected_receiver_temperature == temperatures.T_rx

        # Check that the system temperature has been calculated and the
        # value correctly mapped
        calculate_system_temp_spy.assert_called_once()
        expected_system_temperature = \
            temperatures._calculate_system_temperature(g, t_cmb, eta_eff,
                                                       t_amb, T_atm, tau_atm)
        assert expected_system_temperature == temperatures.T_sys

    def test__calculate_receiver_temperature(self, obs_freq, weather,
                                             elevation, t_cmb, t_amb,
                                             g, eta_eff):

        receiver_temperature = \
            Temperatures._calculate_receiver_temperature(obs_freq)

        # Make sure the temperature is returned in Kelvin
        assert receiver_temperature.unit == "K"

        # Check that the calculated temperature is 5 times the theoretical
        # minimum receiver temperature
        theoretical_min_temp = (constants.h * obs_freq / constants.k_B).to(u.K)
        expected_temp = 5 * theoretical_min_temp
        # Handle rounding errors
        assert round(receiver_temperature.value, 6) == \
               round(expected_temp.value, 6)

    def test__calculate_system_temperature(self, t_cmb, t_amb, g, eta_eff,
                                           weather, elevation):

        band_temps = []

        for obs_freq_band in test_obs_frequency_bands:

            obs_freq = obs_freq_band[0] * u.GHz
            band = obs_freq_band[1]

            atmosphere_params = AtmosphereParams()
            tau_atm = \
                atmosphere_params.calculate_tau_atm(obs_freq, weather,
                                                    elevation)
            T_atm = \
                atmosphere_params.calculate_atmospheric_temperature(obs_freq,
                                                                    weather)
            temperatures = Temperatures(obs_freq, t_cmb, t_amb, g,
                                        eta_eff, T_atm, tau_atm)

            system_temperature = \
                temperatures._calculate_system_temperature(g, t_cmb, eta_eff,
                                                           t_amb, T_atm,
                                                           tau_atm)

            # Confirm that the system temperature is *very* hot for
            # opaque frequencies
            if band == "opaque":
                assert system_temperature > 1e9 * u.K
            else:
                band_temps.append(system_temperature.value)
                assert system_temperature < 1800 * u.K
                print(f'\nband: {band}, temp: {system_temperature}')

        # Confirm that the system temperature follows an increasing trend
        # with the band
        x = np.arange(1, len(band_temps)+1)
        y = np.array(band_temps)
        res = linregress(x, y)
        print(f'Equation: {res[0]:.3f} * x + {res[1]:.3f}')
        assert res[0] > 1
