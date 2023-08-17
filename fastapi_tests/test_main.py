import pytest
from fastapi.testclient import TestClient
from web_client.main import app
from web_client.utils import version_num_for_url

client = TestClient(app)

user_input = {
    't_int': {'value': '100', 'unit': 's'},
    'sensitivity': {'value': '3.0', 'unit': 'mJy'},
    'bandwidth': {'value': '100', 'unit': 'MHz'},
    'obs_freq': {'value': '100', 'unit': 'GHz'},
    'elevation': {'value': '45', 'unit': 'deg'},
    'weather': {'value': '25', 'unit': None},
    'n_pol': {'value': '2', 'unit': None}
}

version = version_num_for_url()


def test_calculate_sensitivity():

    response = client.post(
        f'/v{version}/sensitivity/',
        json=user_input
    )

    assert response.status_code == 200

    sensitivity = response.json()
    assert sensitivity['unit'] == 'uJy'
    assert pytest.approx(sensitivity['value'], 0.01) == 780.


def test_calculate_t_int():
    response = client.post(
        f'/v{version}/integration-time/',
        json=user_input
    )

    assert response.status_code == 200

    integration_time = response.json()
    assert integration_time['unit'] == 's'
    assert pytest.approx(integration_time['value'], 0.1) == 6.80


def test_param_values_units():
    response = client.get(
        f'/v{version}/param-values-units/'
    )

    assert response.status_code == 200

    expected_properties = [
        'default_value', 'default_unit', 'lower_value', 'lower_value_is_floor',
        'upper_value', 'upper_value_is_ceil', 'allowed_values', 'units',
        'data_conversion',
    ]
    expected_properties.sort()

    # Verify that the all the user input parameters are included in the
    # response
    response_data = response.json()
    for key in user_input.keys():
        assert key in response_data
        param_data = response_data[key]
        # Verify that each parameter has all the expected properties
        props = list(param_data.keys())
        props.sort()
        assert props == expected_properties
