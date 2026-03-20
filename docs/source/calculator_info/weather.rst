Weather Calculations
====================

Atmospheric Model Grids
-----------------------

A grid of atmospheric temperature and opacity were calculated using `*am* models <https://zenodo.org/records/13748403>`__ for the Atacama Plateau. These grids contain the Rayleigh-Jeans brightness temperature of the sky, :math:`T_\mathrm{sky}(z=0)` and the sky opacity, :math:`\tau_0`, where these are both calculated at zenith. These are then interpolated to the observing frequency and percentile water column requested in the sensitivity calculator. In order to adjust these to the chosen elevation, the code calculates the atmospheric temperature, :math:`T_\mathrm{atm}`, and transmittance :math:`\mathfrak{t}` as a function of the zenith angle (90°-elevation)
.. math::
    T_\mathrm{atm} = \frac{T_\mathrm{sky}(z=0)}{1-e^{-\tau_0}} 
and the transmittance as a function of the zenith angle (90°-elevation)
.. math::
    \mathfrak{t} = e^{-\tau_0\sec{z}} 

The sky temperature at the chosen elevation is then calculated from these terms. At this stage, the contribution from the temperature of the Cosmic Microwave Background, :math:`T_\mathrm{cmb}`, is also added, noting that this needs to be converted to a Rayleigh-Jeans brightness temperature for consistency.
.. math::
    T_{sky} = (1-\mathfrak{t})\times T_{atm} + O(\nu, T_\mathrm{cmb})
Here, :math:`O(\nu, T)` converts a physical temperature to a Rayleigh-Jeans brightness temperature

.. math::
    O(\nu, T) = T\frac{h\nu/kT}{\exp(h\nu/kT)-1}

where :math:`\nu` is the observing frequency, :math:`h` is the Planck constant and :math:`k` is the Boltzmann constant.



Percentile Water Column
-----------------------

The input required for the calculator is the percentile water column in the atmosphere,
which takes a value between 5 and 95%, with 5% being low water column, and 95% being high.

These percentiles map to the precipitable water vapour (PWV) and ALMA octile weather conditions as
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
