import pytest
import numpy as np
from atlast_sc.sefd import SEFD
import astropy.units as u


def test_SEFD():
    T_sys = 270 * u.K
    radius = 25 * u.m
    area = np.pi * radius**2
    eta_A = 1

    sefd = SEFD.calculate(T_sys, area, eta_A).value

    # This assert statement is currently failing due to the static
    # value being incorrect.
    # TODO These values should be re-calculated by hand to ensure
    # tests are correct and robust.
    assert sefd == pytest.approx(3.797057313069965e-24, 1e-26)
