import pytest

def test_SEFD():
    from atlast_sc.sefd import SEFD 
    import astropy.units as u
    import numpy as np
    T_sys = 270 * u.K
    radius = 25 * u.m
    area = np.pi * radius**2
    eta_A = 1

    sefd = SEFD.calculate(T_sys, area, eta_A).value

    # This assert statement is currently failing due to the static value being incorrect.
    # These values should be re-calculated by hand to ensure tests are correct and robust.
    assert sefd == pytest.approx(3.797057313069965e-24, 1e-26)
