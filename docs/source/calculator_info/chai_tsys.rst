CHAI system temperature
=======================

The CCAT Heterodyne Array Instrument (`CHAI <https://www.ccatobservatory.org/chai/>`__) is being built for the CCAT Observatory. It covers the frequency ranges between 460 and 500 GHz and 780 and 820 GHz. It is set-up to cover channel spacings from 61 kHz to 4 GHz. It has a receiver temperature of 100 K for the lower frequency range and 200 K for the higher frequency range. (See `Barrueto et al. 2023 <https://articles.adsabs.harvard.edu/pdf/2023pcsf.conf..346B>`__ for more details.)

Here in the AtLAST sensitivity calculator, we use it as an exemplar of a heterodyne instrument capable of working at these frequencies.

In this module, we calculate the system temperature used in the overall ::doc::`sensitivity equation <sensitivity>`. For a CHAI like system, the system temperature is calculated as:

.. math::
    T_{sys} = \frac{1}{\eta_{eff} \mathfrak{t}} \times [T_\mathrm{rx} + (\eta_\mathrm{eff} T_\mathrm{sky}) + (1-\eta_\mathrm{eff}) O(\nu, T_\mathrm{amb})]

where

* :math:`\eta_\mathrm{eff}` is the forward efficiency of the telescope
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_\mathrm{rx}` is the receiver temperature
* :math:`T_\mathrm{sky}` is the sky temperature (in terms of a Rayleigh-Jeans brightness temperature) calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_\mathrm{amb}` is the ambient temperature

Here, :math:`O(\nu, T)` converts a physical temperature to a Rayleigh-Jeans brightness temperature

.. math::
    O(\nu, T) = T\frac{h\nu/kT}{\exp(h\nu/kT)-1}.

Through consultation with the developers of the CHAI instrument, we assume a constant receiver temperature across each sub-band the receivers are sensitive to:

.. math::
    T_{rx} = \left\{ \begin{array}{rcl}
            100\,\mbox{K} & \mbox{for} & 460<\nu<500\,\mbox{GHz} \\ 
            200\,\mbox{K} & \mbox{for} & 780<\nu<820\,\mbox{GHz} 
            \end{array}\right.

These values are used in the :math:`T_{sys}` equation above, which is in turn used to calculate the System Equivalent Flux Density used in the overall sensitivity (or integration time) calculation.
