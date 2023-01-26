import pytest
import astropy.units as u
from atlast_sc.system_temperature import SystemTemperature


def test_temperatures():
    T_rx = 50 * u.K
    T_cmb = 2.73 * u.K
    T_atm = 255 * u.K
    T_amb = 270 * u.K
    tau_atm = 0.8

    g = 1
    eta_eff = 0.9

    t = SystemTemperature(T_rx, T_cmb, T_atm, T_amb, tau_atm)
    assert t.system_temperature(g, eta_eff).value == pytest.approx(205.761, 0.001)


def test_units():
    T_rx = 50 * u.K
    T_cmb = 2.73 * u.K
    T_atm = 255 * u.K
    T_amb = 270 * u.K
    tau_atm = 0.8

    g = 1
    eta_eff = 0.9

    t = SystemTemperature(T_rx, T_cmb, T_atm, T_amb, tau_atm)
    assert t.system_temperature(g, eta_eff).unit == "K"

