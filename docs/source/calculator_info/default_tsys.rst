Default instrument system temperature
=====================================

For the parameter space in which there is no pre-defined instrument that can be used to calculate the telescope sensitivity, we default to the more generic representation of a receiver with a specified receiver temperature. This setup is valid for all ranges of observing frequency and bandwidth, and from it, the system temperature is calculated as:

.. math::
    T_{sys} = \frac{1}{\eta_{eff} \mathfrak{t}} \times [T_{rx} + (\eta_{eff} T_{sky}) + (1-\eta_{eff}) T_{amb}]

where

* :math:`\eta_{eff}` is the forward efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_{rx}` is the receiver temperature
* :math:`T_{sky}` is the sky temperature
* :math:`T_{amb}` is the ambient temperature

The receiver temperature is the only instrument dependent component of the above equation, and we assume a reasonably efficient instrument near the quantum limit. Specifically:

.. math::
    T_{rx} = \frac{5h\nu}{k}

where :math:`h` and :math:`k` are the Planck and Boltzmann constants (respectively), :math:`\nu` is the frequency of the observation, and the factor 5 is a conservative estimate of how close to the quantum limit receivers can get. The fundamental limit achievable when including mixer and Local oscillator terms is 3, but most receivers do not achieve that efficiency.

The sky temperature is calculated as:

.. math::
    T_{sky} = (1-\mathfrak{t})\times T_{atm} + T_{cmb}

where

* :math:`T_{atm}` is the atmospheric temperature calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_{cmb}` is the temperature of the cosmic microwave background.
