import pytest
from pydantic import BaseModel
from atlast_sc.models import *


class TestModel(BaseModel):
    value1: ValueWithUnits = ValueWithUnits(value=1, unit='GHz')
    value2: ValueWithUnits = ValueWithUnits(value=2.1234567e10, unit='s')


@pytest.mark.parametrize(
    'model,expect_result',
    [
        (TestModel(), 'hello'),
    ]
)
def test_model_str_rep(model, expect_result):
    # TODO: pick up from here
    print('\n' + model_str_rep(model))
    assert True


def test_create_value_with_units():
    assert True


def test_create_value_without_units():
    assert True




