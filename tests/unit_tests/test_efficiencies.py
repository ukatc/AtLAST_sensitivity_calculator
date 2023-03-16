
def test_eta_s(efficiencies):
    eta_s = efficiencies.eta_s()
    print('got value for eta_s of', eta_s)
    assert eta_s <= 1


def test_eta_a(efficiencies, obs_freq, surface_rms):
    eta_a = efficiencies.eta_a(obs_freq, surface_rms)
    print('got value for eta_a of', eta_a)
    # assert eta_a.value == pytest.approx(0.9211434072170483)
    assert eta_a.value <= 1


def test_ones():
    """
    can write a test here that if all efficiencies are set to 1,
    the resulting efficiency should be 1
    """


def test_zero():
    """
    can write a test here that if any efficience is 0, the resulting
    efficiency should be zero
    """
