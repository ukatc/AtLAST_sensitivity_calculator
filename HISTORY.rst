2.0.0-alpha.1 (2026-03-05)
++++++++++++++++++++++++++
- Refactored code to improve flexibility
- Changed the names and workings of calculation input parameter classes to make more sense with the addition of instrument modules
- Added functionality for instrument modules to be introduced for calculating the system temperature
- Added specific instrument modules to represent CHAI, FINER, MUSCAT, SEPIA, TIFUUN
- Added automatic instrument selection based on observing frequency and bandwidth input by user
- Added instrument selection option on the CLI 
- Added functionality to see if requested instrument can be chosen
- Added functionality to show a list of instruments with their observing frequency and bandwidth ranges
- Made instrument name specification case insensitive
- Modified unit tests according to the new structure
- More explanatory exception messages
- Documentation updates to take account of these changes

1.1.1 (2025-01-22)
++++++++++++++++++
- Updates to readthedocs files to enable readthedocs to display API and UML pages and to automatically create a pdf.
- Update to pydantic and fastapi as these were causing conflicts with anaconda.

1.1.0 (2023-12-12)
++++++++++++++++++
- Integration of the broad band extension, based on the calculation of a band-integrated effective SEFD.

1.0.1 (2023-10-31)
++++++++++++++++++
- Update numpy and astropy requirements so that the calculator is compatible with Python 3.12.
