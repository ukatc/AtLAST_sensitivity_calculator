import pytest
import astropy.units as u

def test_eta_ill():
    from atlast_sc.efficiencies import Efficiencies
    test_ill = 0.5
    eff = Efficiencies(test_ill)
    assert eff.eta_ill == test_ill

def test_eta_s():
    from atlast_sc.efficiencies import Efficiencies
    eff = Efficiencies(0.7)
    eta_s = eff.eta_s()
    assert eta_s <= 1

def test_eta_a():
    from atlast_sc.efficiencies import Efficiencies
    obs_freq = 500 * u.GHz
    surface_rms = 25 * u.micron
    eff = Efficiencies(0.7)
    eta_a = eff.eta_a(obs_freq, surface_rms)
    print(eta_a)
    # assert eta_a.value == pytest.approx(0.9211434072170483)
    assert eta_a.value <= 1
