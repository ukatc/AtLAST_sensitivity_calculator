SEPIA system temperature
========================

The Swedish-ESO PI receiver for APEX (`SEPIA <https://www.apex-telescope.org/ns/observing/the-telescope/instruments/sepia/sepia345/>`__) 345 GHz receiver is being built for the APEX Observatory. It covers the frequency ranges between 272 and 376 GHz. It is set-up to cover channel spacings from 62.5 kHz to 0.18 GHz. It has a receiver temperature that rises from 90 K to 216.5 K. (See `Meledin et al. 2022 <https://www.aanda.org/articles/aa/pdf/2022/12/aa44211-22.pdf>`__ for more details.)

Here in the AtLAST sensitivity calculator, we use it as an exemplar of a heterodyne instrument capable of working at these frequencies.

In this module, we calculate the system temperature used in the overall ::doc::`sensitivity equation <sensitivity>`. For a SEPIA like system, the system temperature is calculated as:

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

Through consultation with the developers of the SEPIA instrument, we assume a receiver temperature that remains constant between observing frequencies of 272 and 330 GHz and then rises up to the maximum frequency of 376 GHz:

.. math::
    T_{rx} = \left\{ \begin{array}{rcl}
            90\,\mbox{K} & \mbox{for} & 272<\nu<330\,\mbox{GHz} \\ 
            90\,\textrm{K}+(216.5\,\textrm{K} - 90\,\textrm{K}) \times\frac{\nu-330\,\textrm{GHz}}{376\,\textrm{GHz}-330\,\textrm{GHz}} & \mbox{for} & 330<\nu<376\,\mbox{GHz} 
            \end{array}\right.

These values are used in the :math:`T_{sys}` equation above, which is in turn used to calculate the System Equivalent Flux Density used in the overall sensitivity (or integration time) calculation.
