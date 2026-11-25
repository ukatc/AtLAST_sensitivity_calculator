2.0.0 (2026-11-25)
++++++++++++++++++
**Code Improvements**

- Created a core package for calculator functionality and modules.
- Added specific instrument modules to represent ALMA and ALMA WSU.
- Added option to supply telescope and environment parameters on the CLI. 
- Re-added the finetune option when creating a calculator object on the CLI (Mistakenly removed in 2.0.0-beta).
- Added functionality to specify instrument preference order in the CLI.
- Changed method of choosing an applicable instrument to consider instrument preference order, if specified.
- Added option to choose viewing calculated sensitivity as a flux density or brightness temperature.
- Added option to supply bandwidth frequency value as velocity.
- Added methods to convert between flux density and temperature (for sensitivity values) and added user-facing methods to do conversion.
- Added methods to convert between velocity and frequency (for bandwidth values) and added user-facing methods to do conversion.
- Added API requests to convert from special units to default units. 
- Added API requests to get applicable instruments and instrument ranges.
- Added API requests to set instruments on the backend. 
- Added conversion of any bandwidth unit to Hz for easier comparison in the backend.

**Testing & Validation**

- Updated test environment image version to Ubuntu 24.04 (was 22.04).
- Updated test environment to Python 3.13 (was 3.10).
- Added validation for the chosen instrument.
- Added validation for instrument preference list.
- Added special unit recognition (for bandwidth and sensitivity values) in validation methods.
- Added tests for added functionalities. 
- Populated Fast API tests.

**Web Client**

- Reorganised the layout into user input area (left) and instrument area (right).
- Added an option to select an instrument to use in the calculations. 
- Added functionality to see available instruments and instrument ranges on the instrument area.
- Added link to instrument documentation on the instrument area.
- Added version number on the header.
- Fixed change of polarisation value not triggering the enability of calculate button. 
- Added cross validation between chosen instrument and inputted observing frequency and bandwidth values.
- Add the option of displaying the calculated sensitivity value in flux density or brightness temperature.
- Updated EU funding acknowledgement. 
- Added new adjustments to keep UI tidy in additional two screen sizes.

**Documentation & User Experience**

- Added documentation for ALMA and ALMA WSU.
- Modified documentation to explain the new package structures.
- Modified documentation to include new special units for bandwidth and sensitivity values. 
- Modified documentation to include instructions on instrument preference order specification.
- Modified documentation to include instructions on how to use unit conversion helper functions.
- Changed Python package installation instructions to correspond to new dependency versions. 
- Removed Docker instructions.


2.0.0-beta (2026-05-29)
++++++++++++++++++++++++++

**Code Improvements**

- Simplified and modularised code structure
- Separated calculation input parameters into categories
- Added error handling when calculator parameters are accessed using the deprecated API.
- Updated test utilities and modified unit tests according to the new structure.
- Added functionality for instrument modules to be introduced for calculating the system temperature.
- Added specific instrument modules to represent CHAI, FINER, MUSCAT, SEPIA, TIFUUN.
- Added automatic instrument selection based on observing frequency and bandwidth input by user.
- Added instrument selection option on the CLI.
- Added functionality to see if requested instrument can be chosen.
- Added functionality to show a list of instruments with their observing frequency and bandwidth ranges.
- Changed default observing frequency to 406 GHz (was 100 GHz).
- More explanatory exception messages.
- Changed am model output to produce Rayleigh-Jeans brightness temperature and to avoid including CMB (to avoid counting it twice).
- Changed system temperature and sky temperature equations to ensure all temperatures are noise temperatures.
- Added notebook walkthroughs for each of the instruments.

**Web Client**

- Updated EU flag image assets
- Minor HTML/template improvements
- Added EU funding acknowledgement

**Documentation & User Experience**

- Added comprehensive quickstart guide.
- Added instrument documentation with dedicated pages for CHAI, FINER, MUSCAT, SEPIA, and TIFUUN system temperature calculations.
- Revised and expanded calculator info and user guide.
- Improved developer guide with sections on adding new instruments and repository overview.
- Added EU funding acknowledgement throughout documentation.
- Reorganised documentation structure for better navigation.
- Added / updated dependencies to ensure documentation could be generated locally.

1.1.3 (2026-04-15)
++++++++++++++++++
- Set a maximum Python version as the calculator is not currently compatible with Python >=3.13.
- Change the installation instructions to specify a specific Python version.

1.1.2 (2026-01-22)
++++++++++++++++++
- Updates to readthedocs files to enable readthedocs to display API and UML pages and to automatically create a pdf.
- Update to pydantic and fastapi as these were causing conflicts with anaconda.

1.1.1 (2025-08-18)
++++++++++++++++++
- Updates to reflect corrections to ensure tau_atm is described correctly as 'atmospheric optical depth'.
- Updates to various documentation files.

1.1.0 (2023-12-12)
++++++++++++++++++
- Integration of the broad band extension, based on the calculation of a band-integrated effective SEFD.

1.0.1 (2023-10-31)
++++++++++++++++++
- Update numpy and astropy requirements so that the calculator is compatible with Python 3.12.
