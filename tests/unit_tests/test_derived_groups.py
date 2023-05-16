from atlast_sc.derived_groups import AtmosphereParams, Temperatures, \
    Efficiencies


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
