import pytest

def test_sensitivity():
    from src.functions.sensitivity import Sensitivity
    from astropy import constants
    import astropy.units as u
    bandwidth = 7.5 * u.GHz

    tau_atm = 0.7
    sefd = 10 * u.K / u.m**2 * (constants.k_B)
    n_pol = 1
    eta_s = 1

    example_t_int = 1 * u.s

    bandwidth = bandwidth.to(u.Hz)

    calculator = Sensitivity(bandwidth, tau_atm, sefd, n_pol, eta_s)

    assert calculator.sensitivity(example_t_int).value == pytest.approx(0.32103973505475175)

def test_integration():
    from src.functions.sensitivity import Sensitivity
    from astropy import constants
    import astropy.units as u
    bandwidth = 7.5 * u.GHz

    tau_atm = 0.7
    sefd = 10 * u.K / u.m**2 * (constants.k_B)
    n_pol = 1
    eta_s = 1
    
    example_sensitivity = 15e-5 * u.Jy

    calculator = Sensitivity(bandwidth, tau_atm, sefd, n_pol, eta_s)

    assert calculator.t_integration(example_sensitivity).value == pytest.approx(4580733.843734454)
