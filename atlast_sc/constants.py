import os
from pathlib import Path

PARENT_PATH = Path(__file__).resolve().parents[0]

STANDARD_INPUTS_PATH = os.path.join(PARENT_PATH, "inputs", "standard")
BENCHMARKING_INPUTS_PATH = os.path.join(PARENT_PATH, "inputs", "benchmarking")
BENCHMARKING_JCMT_PATH = os.path.join(BENCHMARKING_INPUTS_PATH, "JCMT")
BENCHMARKING_APEX_PATH = os.path.join(BENCHMARKING_INPUTS_PATH, "APEX")

STANDARD_SETUP = 'standard'
CUSTOM_SETUP = 'custom'
# TODO: are these benchmarking setups still required?
BENCHMARKING_APEX = 'apex'
BENCHMARKING_JCMT = 'jcmt'

SETUP_INPUTS_FILE = 'setup_inputs.yaml'
DEFAULT_INPUTS_FILE = 'default_inputs.yaml'
