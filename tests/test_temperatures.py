import pytest
import astropy.units as u
from atlast_sc.temperature import Temperature


def test_system_temperatures(obs_freq, t_cmb, t_amb, g, eta_eff):

    T_atm = 255 * u.K
    tau_atm = 0.8

    t = Temperature(obs_freq, t_cmb, T_atm, t_amb, tau_atm)

    sys_temp = t.system_temperature(g, eta_eff)

    # TODO: need a more robust way of testing the values are correct
    # Check the system temperature is correct
    assert sys_temp.value \
           == pytest.approx(222.431, 0.001)

    # Check the system temperature has the correct units
    assert sys_temp.unit == "K"
