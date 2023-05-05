import astropy.units as u
from atlast_sc.derived_groups import Efficiencies

test_obs_freqs = [35, 50, 100, 200,  300, 400, 500, 600, 700, 800, 900, 950]


def test_init(efficiencies, obs_freq, surface_rms, eta_ill, eta_spill,
              eta_block, eta_pol):

    # Check all the params have been correctly mapped
    assert efficiencies._obs_freq == obs_freq
    assert efficiencies._surface_rms == surface_rms
    assert efficiencies._eta_ill == eta_ill
    assert efficiencies._eta_spill == eta_spill
    assert efficiencies._eta_block == eta_block
    assert efficiencies._eta_pol == eta_pol


def test_calculate_eta_a(surface_rms, eta_ill, eta_spill, eta_block, eta_pol):

    eta_As = []
    for obs_freq in test_obs_freqs:
        obs_freq = obs_freq * u.GHz
        efficiencies = Efficiencies(obs_freq, surface_rms, eta_ill, eta_spill,
                                    eta_block, eta_pol)

        eta_a = efficiencies._calculate_eta_a()

        # Check that the dish efficiency has been correctly assigned to the
        # property
        assert eta_a == efficiencies.eta_a

        eta_As.append(eta_a)

    # Check that the dish efficiency, eta_a, decreases with increasing
    # observing frequency
    comparisons = [(x - eta_As[i-1]) < 0 for i, x in enumerate(eta_As)][1:]
    assert all(comparisons)
