The Sensitivity Calculation
===========================

The following is a description of the underlying calculations that the software performs.

The sensitivity of a single dish telescope for an integration time :math:`t` is given by:

.. math::
    \Delta S = \frac{SEFD}{\eta_{s}\sqrt{n_{pol} \Delta \nu t}}

or conversely, to obtain the integration time required for a given sensitivity :math:`\Delta S`, 

.. math::
    t = \left(\frac{SEFD}{ \Delta S  \eta_s }\right)^2 \times \frac{1}{n_{pol} \Delta \nu}


where 

* :math:`SEFD` is the system equivalent flux density
* :math:`\eta_{s}` is the system efficiency
* :math:`n_{pol}` is the number of polarizations
* :math:`\Delta \nu` is the bandwidth


The system equivalent flux density is calculated as:

.. math::
    SEFD = \frac{2kT_{sys}}{\eta_{A}A_{g}}

where

* :math:`k` is the Boltzman constant
* :math:`T_{sys}` is the system temperature
* :math:`\eta_{A}` is the dish efficiency
* :math:`A_{g}` is the geometric dish area

The system temperature is calculated as:

.. math::
    T_{sys} = \frac{1+g}{\eta_{eff} \mathfrak{t}} \times [T_{rx} + (\eta_{eff} T_{sky}) + (1-\eta_{eff}) T_{amb}]

where

* :math:`g` is the sideband ratio
* :math:`\eta_{eff}` is the forward efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_{rx}` is the receiver temperature
* :math:`T_{sky}` is the sky temperature
* :math:`T_{amb}` is the ambient temperature

Here we assume a receiver temperature calculated from:

.. math::
    T_{rx} = \frac{5h\nu}{k}

where

* :math:`h` is the Planck constant

The sky temperature is calculated as:

.. math::
    T_{sky} = (1-\mathfrak{t})\times T_{atm} + T_{cmb}

where

* :math:`T_{atm}` is the atmospheric temperature calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_{cmb}` is the temperature of the cosmic microwave background.


Efficiencies
------------

:math:`\eta_{A}`, the dish efficiency, is given by:

.. math::
    \eta_{A} = \eta_{ill} \times \eta_{spill} \times \eta_{pol} \times \eta_{block} \times exp^{(-\frac{(4\pi \times RMS}{\lambda^2})}


where the exponential term accounts for Ruze losses due to the RMS of the dish surface roughness, and

* :math:`\eta_{ill}` is the illumination efficiency
* :math:`\eta_{spill}` is the spillover efficiency
* :math:`\eta_{pol}` is the polarisation efficiency
* :math:`\eta_{block}` is the lowered efficiency due to blocking


Broad-band Sensitivity
----------------------

For continuum observations, the bandwidth used is very broad. In these cases, :math:`\mathfrak{t}` and :math:`T_{atm}` can vary greatly across the bandwidth and it is no longer appropriate to simply use the value at the central frequency. For this reason, we have implemented an option to integrate across the band that can be activated by intialising the calculator with ``Calculator(finetune=True)``. Instead of rescaling the :math:`SEFD` term by the square root of the bandwidth, it generates an effective :math:`SEFD` by discretizing the :math:`SEFD` estimation over the frequency values from the input atmospheric tables to gain the :math:`SEFD_i` for each discrete frequency :math:`\nu_i` with bandwidth :math:`d\nu_i=0.5[\nu_{i+1}-\nu_{i-1}]`. The output effective :math:`SEFD` to be used in the sensitivity estimation is thus:

.. math::
    SEFD = \sqrt{\Delta \nu/\sum_i(d\nu_i/SEFD_i^2)}

