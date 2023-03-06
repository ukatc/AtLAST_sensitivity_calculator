import pytest


@pytest.fixture(scope='session')
def tmp_output_dir(tmp_path_factory):
    """
    Temporary directory where output files should be stored
    """
    return tmp_path_factory.mktemp('output')
