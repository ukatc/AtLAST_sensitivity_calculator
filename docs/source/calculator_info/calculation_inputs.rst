Inputs to the Calculation
=========================

The table below lists the parameters that are used by the calculator to
calculate the integration time or sensitivity. Units in the table are string
representations of `astropy units <https://docs.astropy.org/en/stable/units/index.html>`__:

.. list-table:: Calculation input parameters
    :widths: 10 10 10 10 10 10
    :header-rows: 1

    * - Parameter
      - Label
      - Default value
      - Default unit
      - Permitted range or values
      - Permitted units
    * - Integration time
      - t_int
      - 100
      - s
      - > 1s
      - s, min, h
    * - Sensitivity
      - sensitivity
      - 0.3
      - mJy
      - > 0
      - uJy, mJy, Jy
    * - Bandwidth
      - bandwidth
      - 100
      - MHz
      - > 0
      - Hz, kHz, MHz, GHz
    * - Observing frequency
      - obs_freq
      - 100
      - GHz
      - 35 - 950
      - GHz
    * - Number of polarizations
      - n_pol
      - 2
      - N/A
      - 1, 2
      - N/A
    * - Percentile water column in the atmosphere
      - weather
      - 25
      - N/A
      - 5 - 95
      - N/A
    * - Elevation
      - elevation
      - 45
      - deg
      - 25 - 85
      - deg
