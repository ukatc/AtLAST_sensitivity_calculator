import pytest


def test_temperatures():
    import astropy.units as u
    from src.functions.system_temperature import SystemTemperature
    T_rx = 50 * u.K
    T_cmb = 2.73 * u.K
    T_atm = 255 * u.K
    T_amb = 270 * u.K
    T_gal = 10 * u.K
    tau_atm = 0.8

    g = 1
    eta_eff = 0.9

    t = SystemTemperature(T_rx, T_cmb, T_atm, T_amb, T_gal)
    assert t.sky_temperature(tau_atm).value == pytest.approx(63.73, 0.01)
    assert t.system_temperature(g, eta_eff, tau_atm).value == pytest.approx(238.856, 0.001)

def test_units():
    import astropy.units as u
    from src.functions.system_temperature import SystemTemperature
    T_rx = 50 * u.K
    T_cmb = 2.73 * u.K
    T_atm = 255 * u.K
    T_amb = 270 * u.K
    T_gal = 10 * u.K
    tau_atm = 0.8

    g = 1
    eta_eff = 0.9

    t = SystemTemperature(T_rx, T_cmb, T_atm, T_amb, T_gal)
    assert t.sky_temperature(tau_atm).unit == "K"
    assert t.system_temperature(g, eta_eff, tau_atm).unit == "K"

