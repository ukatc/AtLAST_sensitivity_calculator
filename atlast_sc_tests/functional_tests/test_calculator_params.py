from scipy.stats import linregress
import numpy as np
import pytest
from pydantic import ValidationError
from astropy import units as u
from astropy import constants
from atlast_sc.calculator import Calculator
from atlast_sc.derived_groups import AtmosphereParams, Temperatures, \
    Efficiencies
from atlast_sc_tests.utils import does_not_raise


class TestCalculationInput:
    unit_exception = 'unitexception'
    value_out_of_range_exception = 'valueoutofrangeexception'
    value_too_high_exception = 'valuetoohighexception'
    value_too_low_exception = 'valuetoolowexception'
    value_not_allowed_exception = 'valuenotallowedexception'

    @pytest.mark.parametrize(
        'input_data,expect_raises,exception_name',
        [
            ({'t_int': {'value': 1, 'unit': 's'}}, does_not_raise(), None),
            ({'t_int': {'value': 1, 'unit': 'min'}}, does_not_raise(), None),
            ({'t_int': {'value': 0.5, 'unit': 'min'}}, does_not_raise(), None),
            ({'t_int': {'value': 1, 'unit': 'h'}}, does_not_raise(), None),
            ({'t_int': {'value': 0, 'unit': 's'}},
             pytest.raises(ValidationError), value_out_of_range_exception),
            ({'t_int': {'value': float('inf'), 'unit': 's'}},
             pytest.raises(ValidationError), value_too_high_exception),
            ({'t_int': {'value': 1, 'unit': 'GHz'}},
             pytest.raises(ValidationError), unit_exception),
            ({'sensitivity': {'value': 1, 'unit': 'uJy'}}, does_not_raise(),
             None),
            ({'sensitivity': {'value': 1, 'unit': 'mJy'}}, does_not_raise(),
             None),
            ({'sensitivity': {'value': 1, 'unit': 'Jy'}}, does_not_raise(),
             None),
            ({'sensitivity': {'value': 0, 'unit': 'uJy'}},
             pytest.raises(ValidationError), value_too_low_exception),
            ({'sensitivity': {'value': float('inf'), 'unit': 'uJy'}},
             pytest.raises(ValidationError), value_too_high_exception),
            ({'sensitivity': {'value': 1, 'unit': 's'}},
             pytest.raises(ValidationError), unit_exception),
            ({'bandwidth': {'value': 200, 'unit': 'Hz'}}, does_not_raise(),
             None),
            ({'bandwidth': {'value': 200, 'unit': 'kHz'}}, does_not_raise(),
             None),
            ({'bandwidth': {'value': 200, 'unit': 'MHz'}}, does_not_raise(),
             None),
            ({'bandwidth': {'value': 200, 'unit': 'GHz'}}, does_not_raise(),
             None),
            ({'bandwidth': {'value': 200, 'unit': 'h'}},
             pytest.raises(ValidationError), unit_exception),
            ({'bandwidth': {'value': 0, 'unit': 'Hz'}},
             pytest.raises(ValidationError), value_too_low_exception),
            ({'bandwidth': {'value': float('inf'), 'unit': 'Hz'}},
             pytest.raises(ValidationError), value_too_high_exception),
            ({'obs_freq': {'value': 200, 'unit': 'GHz'}}, does_not_raise(),
             None),
            ({'obs_freq': {'value': 35, 'unit': 'GHz'}}, does_not_raise(),
             None),
            ({'obs_freq': {'value': 950, 'unit': 'GHz'}}, does_not_raise(),
             None),
            ({'obs_freq': {'value': 200, 'unit': 'Hz'}},
             pytest.raises(ValidationError), unit_exception),
            ({'obs_freq': {'value': 30, 'unit': 'GHz'}},
             pytest.raises(ValidationError), value_out_of_range_exception),
            ({'obs_freq': {'value': 960, 'unit': 'GHz'}},
             pytest.raises(ValidationError), value_out_of_range_exception),
            ({'n_pol': {'value': 1}}, does_not_raise(), None),
            ({'n_pol': {'value': 2}}, does_not_raise(), None),
            ({'n_pol': {'value': 0.5}}, pytest.raises(ValidationError),
             value_not_allowed_exception),
            ({'n_pol': {'value': 3}}, pytest.raises(ValidationError),
             value_not_allowed_exception),
            ({'weather': {'value': 50}}, does_not_raise(), None),
            ({'weather': {'value': 5}}, does_not_raise(), None),
            ({'weather': {'value': 25}}, does_not_raise(), None),
            ({'weather': {'value': 2}},
             pytest.raises(ValidationError), value_out_of_range_exception),
            ({'weather': {'value': 100}},
             pytest.raises(ValidationError), value_out_of_range_exception),
            ({'elevation': {'value': 40, 'unit': 'deg'}}, does_not_raise(),
             None),
            ({'elevation': {'value': 25, 'unit': 'deg'}}, does_not_raise(),
             None),
            ({'elevation': {'value': 85, 'unit': 'deg'}}, does_not_raise(),
             None),
            ({'elevation': {'value': 40, 'unit': 'Hz'}},
             pytest.raises(ValidationError), unit_exception),
            ({'elevation': {'value': 15, 'unit': 'deg'}},
             pytest.raises(ValidationError), value_out_of_range_exception),
            ({'elevation': {'value': 90, 'unit': 'deg'}},
             pytest.raises(ValidationError), value_out_of_range_exception),
        ]
    )
    def test_data_validation_on_init(self, input_data, expect_raises,
                                     exception_name):
        # Ensure that parameters can only be initialised with data within the
        # permitted range (inclusive or exclusive), or with one of the
        # permitted values, and with incorrect units, where applicable

        with expect_raises as e:
            Calculator(input_data)

        if exception_name:
            # The details of the custom exception are buried somewhere
            # in the guts of the pydantic ValidationError, so this check (and
            # others like it) are a bit of a clunky hack. Would be nice to
            # find a more elegant solution
            assert exception_name in str(e.value)


class TestDerivedGroups:

    obs_frequency_bands = [
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

    @pytest.mark.parametrize('obs_freq,band', obs_frequency_bands)
    def test_tau_atm(self, obs_freq, band, weather, atmosphere_params):

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

    @pytest.mark.parametrize('obs_freq,band', obs_frequency_bands)
    def test_atmospheric_temperature(self, obs_freq, band, weather, elevation,
                                     atmosphere_params):

        obs_freq = obs_freq * u.GHz

        temp = atmosphere_params.calculate_atmospheric_temperature(obs_freq,
                                                                   weather)
        tau = atmosphere_params.calculate_tau_atm(obs_freq, weather, 90*u.deg)
        # convert atmospheric temperature to sky temperature at zenith = 0
        temp = temp * (1.00-np.exp(-tau))

        # Check that the atmospheric temperature is "cold" for transparent
        # frequencies and "hot" for opaque frequencies
        if band == "opaque":
            assert temp > 250 * u.K
        else:
            assert temp < 150 * u.K

    def test_receiver_temperature(self, obs_freq, weather, elevation,
                                  t_cmb, t_amb, g, eta_eff):

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

    def test_system_temperature(self, t_cmb, t_amb, g, eta_eff, weather,
                                elevation):

        band_temps = []

        for obs_freq_band in self.obs_frequency_bands:

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

        # Confirm that the system temperature follows an increasing trend
        # with the band
        x = np.arange(1, len(band_temps)+1)
        y = np.array(band_temps)
        res = linregress(x, y)
        # print(f'Equation: {res[0]:.3f} * x + {res[1]:.3f}')
        assert res[0] > 1

    def test_eta_a(self, surface_rms, eta_ill, eta_spill, eta_block, eta_pol):
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
