The Sensitivity Calculation
===========================

The following is a description of the underlying calculations that the software performs. Values for the telescope and environment parameters can be found in the :doc:`Inputs to the Calculation <calculation_inputs>` page.

The sensitivity of a single dish telescope for an integration time :math:`t` is given by:

.. math::
    \Delta S = \frac{SEFD}{\eta_\mathrm{s}\sqrt{n_\mathrm{pol} \Delta \nu t}}

or conversely, to obtain the integration time required for a given sensitivity :math:`\Delta S`, 

.. math::
    t = \left(\frac{SEFD}{ \Delta S  \eta_s }\right)^2 \times \frac{1}{n_\mathrm{pol} \Delta \nu}


where 

* :math:`SEFD` is the system equivalent flux density, a measure of the inherent noise in the observations that comes from the system.
* :math:`\eta_\mathrm{s}` is the system efficiency on a scale of 0 to 1
* :math:`n_\mathrm{pol}` is the number of polarizations
* :math:`\Delta \nu` is the bandwidth of the observation


The system equivalent flux density is calculated as:

.. math::
    SEFD = \frac{2kT_\mathrm{sys}}{\eta_\mathrm{A}A_\mathrm{g}}

where

* :math:`k` is the Boltzmann constant
* :math:`\eta_\mathrm{A}` is the dish efficiency
* :math:`A_\mathrm{g}` is the geometric dish area
* :math:`T_\mathrm{sys}` is the system temperature

The system temperature is calculated differently depending on which instrument is selected for the calculation. Examples of existing instruments for other telescopes have been included in the sensitivity calculator. Specifically, we have included examples of Heterodyne spectroscopic instruments (:doc:`CHAI <chai_tsys>`, :doc:`FINER <finer_tsys>`, and :doc:`SEPIA <sepia_tsys>`), a LEKID based continuum instrument (:doc:`MUSCAT <muscat_tsys>`), and a MKID based IFU (:doc:`TIFUUN <tifuun_tsys>`). The calculator automatically selects the instrument based on the requested observing frequency and channel bandwidth as described in the :doc:`instrument overview <instrument_overview>`.

For the parameter space in which there is no pre-defined instrument that can be used to calculate the telescope sensitivity, we default to the more generic representation of a coherent receiver with a specified receiver temperature. This setup is valid for all ranges of observing frequency and bandwidth, and from it, the system temperature is calculated as:

.. math::
    T_\mathrm{sys} = \frac{1}{\eta_\mathrm{eff} \mathfrak{t}} \times [T_\mathrm{rx} + (\eta_\mathrm{eff} T_\mathrm{sky}) + (1-\eta_\mathrm{eff}) O(\nu, T_\mathrm{amb})]

where

* :math:`\eta_{eff}` is the forward efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_{rx}` is the receiver temperature
* :math:`T_{sky}` is the sky temperature
* :math:`T_{amb}` is the ambient temperature

Here, :math:`O(\nu, T)` converts a physical temperature to a Rayleigh-Jeans brightness temperature

.. math::
    O(\nu, T) = T\frac{h\nu/kT}{\exp(h\nu/kT)-1}

where :math:`\nu` is the frequency of the observation and :math:`h` is the Planck constant.

The receiver temperature is the only instrument dependent component of the above equation, and we assume a reasonably efficient instrument near the quantum limit. Specifically:

.. math::
    T_{rx} = \frac{5h\nu}{k}

where the factor 5 is a conservative estimate of how close to the quantum limit receivers can get. The fundamental limit achievable when including mixer and local oscillator terms is 3, but most receivers do not achieve that efficiency.

The sky temperature is calculated as:

.. math::
    T_{sky} = (1-\mathfrak{t})\times T_{atm} + \mathfrak{t} O(\nu, T_\mathrm{cmb})

where

* :math:`T_{atm}` is the atmospheric temperature calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_{cmb}` is the temperature of the cosmic microwave background.




Efficiencies
------------

No system is 100% efficient, and efficiency terms are used in the sensitivity calculations to reflect inefficiencies in the real world systems. These unitless efficiencies (:math:`\eta`) are scaled from 0 (completely inefficient) to 1 (completely efficient). Below we describe the efficiencies used in the calculator

:math:`\eta_{A}`, the dish efficiency, is given by:

.. math::
    \eta_{A} = \eta_{ill} \times \eta_{spill} \times \eta_{pol} \times \eta_{block} \times e^{(-(\frac{4\pi \times RMS}{\lambda})^2)}


where the exponential term accounts for Ruze losses due to the RMS surface accuracy of the dish, and

* :math:`\eta_{ill}` is the illumination efficiency
* :math:`\eta_{spill}` is the spillover efficiency
* :math:`\eta_{pol}` is the polarisation efficiency
* :math:`\eta_{block}` is the lowered efficiency due to blocking

The values of these efficiencies used in the calculator can be found via the telescope parameters in the tables in :doc:`calculation_inputs`, by issuing the ``calculator.telescope_and_environment.show()`` command after creating a calculator instance in python, or by inspecting the values in ``data.py`` in the source code.

Broad-band Sensitivity
----------------------

For continuum observations, the bandwidth used can be very broad. In these cases, :math:`\mathfrak{t}` and :math:`T_{atm}` can vary greatly across the bandwidth and it is no longer appropriate to simply use the value at the central frequency. For this reason, we have implemented an option to integrate across the band that can be activated by initialising the calculator with ``Calculator(finetune=True)``. Instead of rescaling the :math:`SEFD` term by the square root of the bandwidth, it generates an effective :math:`SEFD` by discretizing the :math:`SEFD` estimation over the frequency values from the input atmospheric tables to gain the :math:`SEFD_i` for each discrete frequency :math:`\nu_i` with bandwidth :math:`d\nu_i=0.5[\nu_{i+1}-\nu_{i-1}]`. The output effective :math:`SEFD` to be used in the sensitivity estimation is thus:

.. math::
    SEFD = \sqrt{\Delta \nu/\sum_i(d\nu_i/SEFD_i^2)}

