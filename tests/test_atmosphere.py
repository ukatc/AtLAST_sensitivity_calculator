import astropy.units as u
import numpy as np
from pathlib import Path
import pytest

def test_init():
    from src.functions.atmosphere_params import AtmosphereParams
    obs_freq = 400 * u.GHz
    pwv = 50
    elevation = 20 * u.deg
    atm = AtmosphereParams(obs_freq, pwv, elevation)
    assert atm.tau_atm_table[0,0] == 30
    assert atm.T_atm_table[0,0] == 30

def test_tau_atm():
    from src.functions.atmosphere_params import AtmosphereParams
    obs_freq = 500 * u.GHz
    pwv = 50
    elevation = 20 * u.deg
    atm = AtmosphereParams(obs_freq, pwv, elevation)
    zenith = 90.0 * u.deg - elevation

    assert (atm.tau_atm().value < 1.0419/np.cos(zenith)) and (atm.tau_atm().value > 1.040/np.cos(zenith))


def test_T_atm():
    from src.functions.atmosphere_params import AtmosphereParams
    obs_freq = 500 * u.GHz
    pwv = 50
    elevation = 20 * u.deg
    atm = AtmosphereParams(obs_freq, pwv, elevation)

    assert (atm.T_atm().value > 173.668) and (atm.T_atm().value < 173.766)
