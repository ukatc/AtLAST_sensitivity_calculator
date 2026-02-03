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

* :math:`SEFD` is the system equivalent flux density, a measure of the inherent noise in the observations that comes from the system.
* :math:`\eta_{s}` is the system efficiency on a scale of 0 to 1
* :math:`n_{pol}` is the number of polarizations
* :math:`\Delta \nu` is the bandwidth of the observation


The system equivalent flux density is calculated as:

.. math::
    SEFD = \frac{2kT_{sys}}{\eta_{A}A_{g}}

where

* :math:`k` is the Boltzman constant
* :math:`\eta_{A}` is the dish efficiency
* :math:`A_{g}` is the geometric dish area
* :math:`T_{sys}` is the system temperature

The system temperature is dependent on sky transmittance and includes terms from both the telescope and selected reciever/instrumet. The system temperature is calculated differently depending on which instrument is selected for the calculation. These equations are described in the following pages:

* :doc:`Default heterodyne <default_tsys>`
* :doc:`CHAI <chai_tsys>`
* :doc:`TIFUUN <tifuun_tsys>`


Efficiencies
------------

No system is 100% efficient, and efficiency terms are used in the sensitivty calculations to reflect in-efficiencies in the real world systems. These unitless efficiencies (:math:`\eta`) are scaled from 0 (completely inefficient) to 1 (completely efficient). Below we describe the efficiencies used in the calculator

:math:`\eta_{A}`, the dish efficiency, is given by:

.. math::
    \eta_{A} = \eta_{ill} \times \eta_{spill} \times \eta_{pol} \times \eta_{block} \times exp^{(-(\frac{4\pi \times RMS}{\lambda})^2)}


where the exponential term accounts for Ruze losses due to the RMS of the dish surface accuracy, and

* :math:`\eta_{ill}` is the illumination efficiency
* :math:`\eta_{spill}` is the spillover efficiency
* :math:`\eta_{pol}` is the polarisation efficiency
* :math:`\eta_{block}` is the lowered efficiency due to blocking


Broad-band Sensitivity
----------------------

For continuum observations, the bandwidth used is very broad. In these cases, :math:`\mathfrak{t}` and :math:`T_{atm}` can vary greatly across the bandwidth and it is no longer appropriate to simply use the value at the central frequency. For this reason, we have implemented an option to integrate across the band that can be activated by intialising the calculator with ``Calculator(finetune=True)``. Instead of rescaling the :math:`SEFD` term by the square root of the bandwidth, it generates an effective :math:`SEFD` by discretizing the :math:`SEFD` estimation over the frequency values from the input atmospheric tables to gain the :math:`SEFD_i` for each discrete frequency :math:`\nu_i` with bandwidth :math:`d\nu_i=0.5[\nu_{i+1}-\nu_{i-1}]`. The output effective :math:`SEFD` to be used in the sensitivity estimation is thus:

.. math::
    SEFD = \sqrt{\Delta \nu/\sum_i(d\nu_i/SEFD_i^2)}

