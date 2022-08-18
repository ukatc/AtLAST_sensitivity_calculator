The sensitivity calculation
===========================

The following is a desription of the underlying calculations that the software perform.

The sensitivity of a single dish telescope for an integration time :math:`t` is given by:

.. math::
    \Delta S = \frac{SEFD}{\eta_{s}\sqrt{n_{pol} \Delta \nu t}} \times \textrm{exp}^{\tau_{atm}}

or conversely, to obtain the integration time required for a given sensitivity :math:`\Delta S`, 

.. math::
    t = \left(\frac{SEFD}{ \Delta S  \eta_s \textrm{exp}^{\tau_{atm}}}\right)^2 \times \frac{1}{n_{pol} \Delta \nu} 


where 

* :math:`SEFD` is the system equivalent flux density
* :math:`\eta_{s}` is the system efficiency
* :math:`n_{pol}` is the number of polarizations
* :math:`\Delta \nu` is the bandwidth
* :math:`\tau_{atm}` is the atmospheric opacity


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
    T_{sys} = \frac{1+g}{\eta_{eff} \mathfrak{t}} \times T_{rx} + (\eta_{eff} T_{sky}) + (1-\eta_{eff}) T_{amb}

where

* :math:`g` is the sideband ratio
* :math:`\eta_{eff}` is the forward efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_{rx}` is the receiver temperature
* :math:`T_{sky}` is the sky temperature
* :math:`T_{amb}` is the ambient temperature