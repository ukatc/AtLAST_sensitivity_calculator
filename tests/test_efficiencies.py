import pytest
import astropy.units as u

def test_eta_ill():
    from atlast_sc.efficiencies import Efficiencies
    test_ill = 0.5
    eta_q = 1
    eta_spill = 1
    eta_block = 1
    eta_pol = 1
    eta_r = 1
    eff = Efficiencies(test_ill, eta_q, eta_spill, eta_block, eta_pol, eta_r)
    assert eff.eta_ill == test_ill

def test_eta_s():
    from atlast_sc.efficiencies import Efficiencies
    eff = Efficiencies(1,1,1,1,1,1)
    eta_s = eff.eta_s()
    assert eta_s <= 1

def test_eta_a():
    from atlast_sc.efficiencies import Efficiencies
    obs_freq = 500 * u.GHz
    surface_rms = 25 * u.micron
    eff = Efficiencies(0.7,1,1,1,1,1)
    eta_a = eff.eta_a(obs_freq, surface_rms)
    print(eta_a)
    # assert eta_a.value == pytest.approx(0.9211434072170483)
    assert eta_a.value <= 1

def test_ones():
    '''
    can write a test here that if all efficiencies are set to 1, the resulting efficiency should be 1
    '''

def test_zero():
    '''
    can write a test here that if any efficience is 0, the resulting efficiency should be zero
    '''
    

    