Weather Calculations
--------------------

A grid of atmospheric temperature and opacity were calculated using *am* models for the Atacama Plateau,
and are interpolated to the observing frequency and water column requested in the sensitivity calculator.

The input required for the calculator is the percentile water column in the atmosphere,
which takes a value between 5 and 95%, with 5% being low water column, and 95% being high.

These percentiles map to the precipitable water vapor (PWV) and ALMA octile weather conditions as
described in the table below.

The water profile/PWV values without equivalent ALMA octiles are those
provided as anchor points in the *am* code - from which the extrapolations are derived.

.. list-table:: Percentile water column to PWV and ALMA octile weather conditions
    :widths: 10 10 10
    :header-rows: 1

    * - Water Profile
        - (%)
      - PWV
        - (mm)
      - Equiv. ALMA Octile
    * - 5.00
      - 0.384
      -
    * - 8.10
      - 0.472
      - 1
    * - 14.65
      - 0.658
      - 2
    * - 23.63
      - 0.913
      - 3
    * - 25.00
      - 0.952
      -
    * - 33.54
      - 1.262
      - 4
    * - 48.24
      - 1.796
      - 5
    * - 50.00
      - 1.86
      -
    * - 61.21
      - 2.748
      - 6
    * - 75.00
      - 3.84
      -
    * - 80.73
      - 5.186
      - 7
    * - 90.00
      - 8.54
      -
