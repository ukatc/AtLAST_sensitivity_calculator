# import pytest


# def test_system_temperatures(temperatures, g, eta_eff):
#
#     sys_temp = temperatures.system_temperature(g, eta_eff)
#
#     # TODO: need a more robust way of testing the values are correct
#     # Check the system temperature is correct
#     assert sys_temp.value \
#            == pytest.approx(222.431, 0.001)
#
#     # Check the system temperature has the correct units
#     assert sys_temp.unit == 'K'

#
# def test_receiver_temperature(temperatures):
#
#     t_rx = temperatures.T_rx
#
#     # TODO: need a more robust way of testing the values are correct
#     # Check the temperature is correct
#     assert t_rx.value == pytest.approx(50, 0.1)
#
#     # Check the receiver temperature has the correct units
#     assert t_rx.unit == 'K'
