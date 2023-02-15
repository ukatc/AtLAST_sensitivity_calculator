import os
from pathlib import Path

PARENT_PATH = Path(__file__).resolve().parents[0]

STANDARD_CONFIG_PATH = os.path.join(PARENT_PATH, "configs", "standard")
BENCHMARKING_CONFIGS_PATH = os.path.join(PARENT_PATH, "configs", "benchmarking")
BENCHMARKING_JCMT_PATH = os.path.join(BENCHMARKING_CONFIGS_PATH, "JCMT")
BENCHMARKING_APEX_PATH = os.path.join(BENCHMARKING_CONFIGS_PATH, "APEX")

STANDARD_SETUP = 'standard'
CUSTOM_SETUP = 'custom'
# TODO: are these benchmarking setups still required?
BENCHMARKING_APEX = 'apex'
BENCHMARKING_JCMT = 'jcmt'
