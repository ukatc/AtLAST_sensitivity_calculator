ALMA system temperature
=======================

The Atacama Large Millimeter/submillimeter Array (`ALMA <https://almascience.eso.org/>`__) is an interferometer on the Chajnantor Plateau. It has dual polarisation heterodyne receivers that cover 10 bands from 35 to 950 GHz. It is set-up to cover channel spacings from 15.25 kHz to 7.5 GHz. The receiver temperatures for each band are shown in a table below. (See `Cortes et al. 2026 <https://almascience.eso.org/documents-and-tools/cycle13/alma-technical-handbook>`__ for more details.) 

ALMA is about undergo a Wideband Sensitivity Upgrade (WSU) and so we also include a module that demonstrates the expected improvements from this (the numbers for this are from `Santander-Vela et al. 2022 <https://www.eso.org/sci/facilities/alma/developmentstudies/ALMAFEDigitizerWGreportdraft220220909.pdf>`__ and `ALMA memo 621 <https://library.nrao.edu/public/memos/alma/main/memo621.pdf>`__). This will decrease the smallest channel spacing to 13.5 kHz. The maximum instantaneous bandwidth has not yet been decided so here we will assume the goal of 32 GHz. The receiver temperature requirements are also included in the table. 

Here in the AtLAST sensitivity calculator, we use it as an exemplar of a heterodyne instrument capable of working at these frequencies.

In this module, we calculate the system temperature used in the overall :doc:`sensitivity equation <../sensitivity>`. For an ALMA like system, the system temperature is calculated as:

.. math::
    T_{sys} = \frac{1+g}{\eta_\mathrm{eff} \mathfrak{t}} \times [T_\mathrm{rx} + (\eta_\mathrm{eff} T_\mathrm{sky}) + (1-\eta_\mathrm{eff}) O(\nu, T_\mathrm{amb})]

where

* :math:`g` is the sideband ratio, which is 0 for bands 1-8 and 1 for bands 9 and 10 of the current ALMA receivers; for the WSU it is 0 for all receivers
* :math:`\eta_\mathrm{eff}` is the forward efficiency of the telescope
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_\mathrm{rx}` is the receiver temperature
* :math:`T_\mathrm{sky}` is the sky temperature (in terms of a Rayleigh-Jeans brightness temperature) calculated from the model grid described in :doc:`Weather Calculations <../weather>`
* :math:`T_\mathrm{amb}` is the ambient temperature

Here, :math:`O(\nu, T)` converts a physical temperature to a Rayleigh-Jeans brightness temperature

.. math::
    O(\nu, T) = T\frac{h\nu/kT}{\exp(h\nu/kT)-1}.

The receiver temperatures for each band for both ALMA and ALMA WSU are shown in the following table. We assume a constant receiver temperature across each sub-band the receivers are sensitive to. For ALMA these are measured receiver temperatures, whereas for ALMA WSU these are the required maximum receiver temperatures (the final receiver temperatures may be significantly lower than these). Note that for cases where the bands overlap, the lowest receiver temperature is used.

+------+-------------------------+---------------------------+-------------------------+---------------------------+
|      | ALMA                                                | ALMA WSU                                            |
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| Band | :math:`\nu` range (GHz) | :math:`T_\mathrm{rx}` (K) | :math:`\nu` range (GHz) | :math:`T_\mathrm{rx}` (K) |
+======+=========================+===========================+=========================+===========================+
| 1    |                   35-52 |                   28      |                   35-52 |                    28     | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 2    |                  67-116 |                        40 |                  67-116 |                        30 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 3    |                  84-116 |                        40 |                  84-116 |                        35 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 4    |                 125-163 |                        42 |                 125-163 |                        40 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 5    |                 158-211 |                        50 |                 158-211 |                        41 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 6    |                 211-275 |                        50 |                 209-281 |                        53 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 7    |                 275-373 |                        72 |                 275-373 |                        72 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 8    |                 385-500 |                       135 |                 385-500 |                       120 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 9    |                 602-720 |                   105     |                 602-720 |                       242 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+
| 10   |                 787-950 |                  230      |                 787-950 |                       365 | 
+------+-------------------------+---------------------------+-------------------------+---------------------------+

These values are used in the :math:`T_{sys}` equation above, which is in turn used to calculate the System Equivalent Flux Density used in the overall sensitivity (or integration time) calculation.
