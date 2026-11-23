Using the Web Client
++++++++++++++++++++
The web client presents a simple user interface to the Python backend. There are six parameters that are needed for the calculation: elevation angle, observing frequency, bandwidth, H\ :sub:`2`\ O percentile profile, number of polarisations and either integration time or sensitivity. Below each input box, the range of acceptable parameters is indicated. For bandwidth, integration time and sensitivity there are a choice of units selectable from the dropdown menu.

[screenshot with initial view]

On the right-hand side, the instrument selection box is shown. This is split into two parts. The top part provides a dropdown menu with all supported instrument options (see :doc:`the instrument overview <../calculator_info/instrument_overview>` for further details) and information on which instruments are applicable to the current setup (based on the observing frequency and bandwidth). The bottom part provides the observing frequency and bandwidth ranges for the currently selected instrument. If an instrument is selected that isn't applicable to the current observing setup, the observing frequency and bandwidth will need to be changed to a value within the ranges shown before a calculation can be made. The supported instruments include high-resolution spectrometers, wide-band IFUs and continuum cameras. In reality, the continuum cameras have a fixed observing frequency and bandwidth - for the currently supported cameras, these are 275 GHz observing frequency with 50 GHz bandwidth for MUSCAT and 90 GHz observing frequency with 26 GHz bandwidth for MISTRAL. However, we have allowed some flexibility in the calculator to test out variations on these instruments.

[screenshot with dropdown menu (if possible - I can't seem to do it on Ubuntu)]

The default mode is to calculate an integration time based on a sensitivity. This can be switched at the bottom of the screen to calculate a sensitivity based on an integration time, in which case the sensitivity user input changes to integration time. When sensitivity is given as an output, there is an option to switch between flux density (in Jy) and brightness temperature (in K).

[screenshot with sensitivity as output]

When the parameters and instrument are set as desired, the calculation can be made using the calculate button at the bottom. A reset button is also provided to switch back to the initial set-up.

