FINER system temperature
========================

The Far-Infrared Nebular Emission Receiver (`FINER <https://finerreceiver.github.io/>`__) is being built for the LMT Observatory. It covers the frequency ranges between 120 and 360 GHz. It is set-up to cover channel spacings from 88 kHz to 0.18 GHz. It has a receiver temperature of 45 K for the lower frequency range and 75 K for the higher frequency range. (See `Tamura et al. 2024 <https://arxiv.org/abs/2406.07975>`__ for more details.)

Here in the AtLAST sensitivity calculator, we use it as an exemplar of a heterodyne instrument capable of working at these frequencies.

In this module, we calculate the system temperature used in the overall :doc:`sensitivity equation <sensitivity>`. For a FINER like system, the system temperature is calculated as:

.. math::
    T_{sys} = \frac{1}{\eta_\mathrm{eff} \mathfrak{t}} \times [T_\mathrm{rx} + (\eta_\mathrm{eff} T_\mathrm{sky}) + (1-\eta_\mathrm{eff}) O(\nu, T_\mathrm{amb})]

where

* :math:`\eta_\mathrm{eff}` is the forward efficiency of the telescope
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`
* :math:`T_\mathrm{rx}` is the receiver temperature
* :math:`T_\mathrm{sky}` is the sky temperature (in terms of a Rayleigh-Jeans brightness temperature) calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_\mathrm{amb}` is the ambient temperature

Here, :math:`O(\nu, T)` converts a physical temperature to a Rayleigh-Jeans brightness temperature

.. math::
    O(\nu, T) = T\frac{h\nu/kT}{\exp(h\nu/kT)-1}.

Through consultation with the developers of the FINER instrument, we assume a constant receiver temperature across each sub-band the receivers are sensitive to:

.. math::
    T_{rx} = \left\{ \begin{array}{rcl}
            45\,\mbox{K} & \mbox{for} & 120<\nu<210\,\mbox{GHz} \\ 
            75\,\mbox{K} & \mbox{for} & 210<\nu<360\,\mbox{GHz} 
            \end{array}\right.

These values are used in the :math:`T_{sys}` equation above, which is in turn used to calculate the System Equivalent Flux Density used in the overall sensitivity (or integration time) calculation.
