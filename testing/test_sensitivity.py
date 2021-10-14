import pytest

def test_sensitivity():
    from src.functions.sensitivity import Calculator
    from astropy import constants
    import astropy.units as u
    bandwidth = 7.5 * u.GHz

    tau_atm = 0.7
    sefd = 10 * u.K / u.m**2 * (constants.k_B)
    n_pol = 1
    eta_s = 1

    example_t_int = 1 * u.s
    example_sensitivity = 15e-5 * u.Jy

    bandwidth = bandwidth.to(u.Hz)

    calculator = Calculator(bandwidth, tau_atm, sefd, n_pol, eta_s)

    assert calculator.calc_sensitivity(example_t_int).value == 0.32103973505475175
    assert calculator.calc_t_integration(example_sensitivity).value == 4580733.843734454

def test_SEFD():
    from src.functions.calculations import SEFD 
    import astropy.units as u
    import numpy as np

    T_sys = 270 * u.K
    radius = 25 * u.m
    area = np.pi * radius**2
    eta_A = 1

    sefd = SEFD.calculate(T_sys, area, eta_A).value
    assert sefd == 3.797057313069965e-24