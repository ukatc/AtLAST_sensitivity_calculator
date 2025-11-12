# Instrument File Upload Instructions

This document provides instructions for uploading new instrument files so that the calculator can recognise and process them correctly.

## Supported File Format
- Instrument files must have two parts to them: one Python file, one YAML file. The Python file should be under the `atlast_sc/instruments/classes` directory and the YAML file should be under the `atlast_sc/instruments/data` directory.

- The Python file for the instrument can be created by copying the `Default.py` file and modifying any of the "Additional instrument specific methods". 
- The YAML file should contain the following columns:
  - `name`: Name of the instrument.
  - `allowed_ranges`: Observing frequency and bandwidth value ranges of the instrument.
  - `receiver_temperature`: Allowed receiver temperature values or value ranges. 

  The `allowed_ranges` column should also contain two sub-columns:
  - `observing_frequency` with two sub-columns `ranges` and `unit`.
  - `bandwidth` with two sub-columns `ranges` and `unit`.

## Upload Instructions
1. Prepare your instrument YAML file in the required format.
2. Ensure all mandatory columns are present and correctly filled.
3. Save the file with the name of the instrument, e.g., `Test.yaml`.
4. Upload the file to the designated `atlast_sc/instruments/data` directory.
5. Prepare your instrument Python file in the required format.
6. Ensure the file is formatted correctly. 
7. Save the file with the name of the instrument, e.g., `Test.py`.
8. Upload the file to the designated `atlast_sc/instruments/classes` directory.
9. Restart the calculator application to load the new instrument data.

## Validation
- Currently there is no validation being performed.

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
  values: [900.0-7500.0]
  unit: K

```