# Instructions for Including a New Instrument

This document provides instructions for adding the files that allow a new instrument to be included in the calculator in a way that ensures the calculator can recognise and process them correctly.

## Supported File Format
- Instrument files must have two parts to them: one Python file, one YAML file. The Python file should be under the `atlast_sc/instruments/classes` directory and the YAML file should be under the `atlast_sc/instruments/data` directory.

- The Python file for the instrument can be created by copying the `.py` file for one of the current instruments and modifying any of the "Additional instrument specific methods". If you are working with a heterodyne instrument, we recommend looking at the files for Default, FINER, CHAI or SEPIA. If you are working with a KID instrument, then we recommend looking at the files for TIFUUN or MUSCAT.
- The YAML file requires the following mandatory keys:
  - `name`: Name of the instrument.
  - `allowed_ranges`: Observing frequency and bandwidth value ranges of the instrument.
  The `allowed_ranges` key should also contain two sub-keys:
  - `observing_frequency` with two sub-keys `ranges` and `unit`.
  - `bandwidth` with two sub-keys `ranges` and `unit`.

- Following these, any parameters used by the instrument class in the `.py` file should be defined, e.g.:
  - `receiver_temperature`: Allowed receiver temperature values or value ranges. 
  These are required to have the sub-key `values`, which should either be a scalar or an array with the same number of values as the `observing_frequency` ranges.
  These can also have the sub-key `unit`, where this must be a unit recognised by `astropy`. For unitless parameters, simply omit this.

## Steps for adding an instrument
1. Prepare your instrument YAML file in the required format.
2. Ensure all mandatory keys are present and correctly filled.
3. Save the file with the name of the instrument, e.g., `Test.yaml`.
4. Add the file to the designated `atlast_sc/instruments/data` directory.
5. Prepare your instrument Python file in the required format.
6. Save the file with the name of the instrument, e.g., `Test.py`.
7. Add the file to the designated `atlast_sc/instruments/classes` directory.
8. Edit the `config.py` in the `atlast_sc/instruments/` directory, adding the new instrument where indicated in `def __init__`.
9. Restart the calculator application to load the new instrument data.

## Documentation
A page describing the new instrument and its system temperature calculation can be added the documentation in the directory `docs/source/calculator_info`. See the other instrument pages for the required format. This should be linked to in the `instrument_overview.rst` and `sensitivity.rst` pages in the same directory.

## Instrument Walkthrough Notebook
If you would like to add a Jupyter notebook to demonstrate the usage of the new instrument, please do so in the `Jupyter_Notebooks/Instrument_Walkthroughs` directory.

## Validation
Currently there is no validation being performed.

## Example
Test.yaml
```

name: "Test"
allowed_ranges:
  observing_frequency:
    ranges: [(90.0-200.0)]
    unit: GHz
  bandwidth: 
    ranges: [(1050.0-30000.0)]
    unit: MHz
receiver_temperature: 
  values: 110.0
  unit: K

```