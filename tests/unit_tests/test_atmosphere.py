# import numpy as np
# import astropy.units as u


def test_init(atmosphere_params):
    assert atmosphere_params.tau_atm_table[0, 0] == 30
    assert atmosphere_params.T_atm_table[0, 0] == 30


# def test_tau_atm(atmosphere_params, elevation):
#
#     zenith = 90.0 * u.deg - elevation
#
#     assert (atmosphere_params.tau_atm().value < 1.0419/np.cos(zenith)) \
#            and (atmosphere_params.tau_atm().value > 1.040/np.cos(zenith))
#
#
# def test_T_atm(atmosphere_params):
#     assert (atmosphere_params.T_atm().value > 173.668) \
#            and (atmosphere_params.T_atm().value < 173.766)
