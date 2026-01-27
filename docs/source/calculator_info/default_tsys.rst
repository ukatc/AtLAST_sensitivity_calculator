Default instrument system temperature
==================

The default instrument is a heterodyne instrument with a receiver temperature that increases as a function of frequency. It is valid for all ranges of observing frequency and bandwidth. The system temperature is calculated as:

.. math::
    T_{sys} = \frac{1}{\eta_{eff} \mathfrak{t}} \times [T_{rx} + (\eta_{eff} T_{sky}) + (1-\eta_{eff}) T_{amb}]

where

* :math:`\eta_{eff}` is the forward efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_{rx}` is the receiver temperature
* :math:`T_{sky}` is the sky temperature
* :math:`T_{amb}` is the ambient temperature

Here we assume a receiver temperature calculated from:

.. math::
    T_{rx} = \frac{5h\nu}{k}

where the factor of 5 is a conservative estimate of the receiver temperature that could be reached and

* :math:`h` is the Planck constant

The sky temperature is calculated as:

.. math::
    T_{sky} = (1-\mathfrak{t})\times T_{atm} + T_{cmb}

where

* :math:`T_{atm}` is the atmospheric temperature calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_{cmb}` is the temperature of the cosmic microwave background.