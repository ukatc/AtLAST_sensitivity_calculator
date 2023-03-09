import pytest


def test_SEFD(sefd):
    # TODO These values should be re-calculated by hand to ensure
    #   tests are correct and robust.
    assert sefd.value == pytest.approx(3.797057313069965e-24, 1e-26)
