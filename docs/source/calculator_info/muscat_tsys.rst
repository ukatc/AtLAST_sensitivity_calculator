MUSCAT system temperature
=========================

Mexico-UK Submillimetre Camera for Astronomy (`MUSCAT <https://muscat-docs.astro.cf.ac.uk/>`__) is being built for the LMT Observatory. MUSCAT is a KID (Kinetic Inductance Detector) instrument. It covers the frequency range between 250 and 300 GHz. It is designed as a broadband instrument with a 50 GHz bandwidth. (See `Tapia et al. 2020 <https://arxiv.org/pdf/2012.05126>`__ for more details.)
To allow for some flexibility, it is set-up in the sensitivity calculator to cover bandwidths from 10 to 80 GHz.  
MUSCAT is being used to demonstrate the capabilities of a KID based continuum camera that can observe at these frequencies on AtLAST.

As a KID instrument, the sensitivity is calculated slightly differently to the heterodyne instruments as Poisson noise and quasiparticle recombination noise are important in addition to the wave noise, as described in detail in this `note <https://github.com/ukatc/AtLAST_sensitivity_calculator/wiki/Sensitivity-Calculation-for-a-Single%E2%80%90mode-KID-based-Instrument>`__. Re-arranging the equations, we find that we can incorporate this instrument into our :doc:`sensitivity calculation <sensitivity>` by determining an equivalent system temperature that is dependent on the Noise Equivalent Power (NEP) as follows:

.. math::
    T_{sys} = \frac{\mathrm{NEP}}{k\,\eta_\mathrm{chip,co}\,\eta_\mathrm{eff}\,\mathfrak{t}\,\sqrt{2n_\mathrm{pol}\,\Delta\nu} }

where

* :math:`\eta_\mathrm{eff}` is the forward efficiency
* :math:`\eta_\mathrm{chip,co}` is the combination of the chip optical efficiency and cold optics optical efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}`

The Noise Equivalent Power is the square root of the sum of the Poisson noise, bunching (wave) noise and quasiparticle recombination noise and calculated as:

.. math::
    \mathrm{NEP} = \sqrt{2\,P_\mathrm{KID}\,h\,\nu+2\,P_\mathrm{KID}^2/(n_\mathrm{pol}\Delta \nu)+4\,\Delta_\mathrm{g}\,P_\mathrm{KID}/\eta_{pb}}

where

* :math:`\Delta_\mathrm{g}` is the gap energy of the superconductor
* :math:`\eta_\mathrm{pb}` is the pair-breaking efficiency
* :math:`P_\mathrm{KID}` is the power received by the KID.

The power received by the KID (:math:`P_\mathrm{KID}`) is dependent on the power spectral density (:math:`PSD_\mathrm{KID}`), which is the sum of the contributions of the noise sources and calculated as:

.. math::
    P_\mathrm{KID}(\nu_\mathrm{0}) = \int^{\nu_\mathrm{max}}_{\nu_\mathrm{min}} PSD_\mathrm{KID}(\nu)\: d\nu \sim PSD_\mathrm{KID}(\nu_\mathrm{0}) \Delta \nu
    
    PSD_\mathrm{KID}(\nu) = &+ \eta_\mathrm{chip,co}(1-\eta_\mathrm{eff})\cdot h\nu\cdot O(\nu, T_\mathrm{amb})\\
                            &+ \eta_\mathrm{chip,co}\,\eta_\mathrm{eff}(1-t_\mathrm{r})\cdot h\nu\cdot O(\nu, T_\mathrm{atm})\\
                            &+ \eta_\mathrm{chip,co}\,\eta_\mathrm{eff}\,t_\mathrm{r}\cdot h\nu\cdot O(\nu, T_\mathrm{cmb})

where 

* :math:`T_\mathrm{atm}` is the atmospheric temperature calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_\mathrm{cmb}` is the temperature of the cosmic microwave background
* :math:`T_\mathrm{amb}` is the ambient temperature.

Here, :math:`O(\nu, T)` is the Bose-Einstein photon-occupation number

.. math::
    O(\nu, T) = \frac{1}{\exp(h\nu/kT)-1}.

For MUSCAT, the constants are expected to have the following values (based on information provided by the MUSCAT team):

* :math:`\eta_\mathrm{chip_co} = 0.5`
* :math:`\Delta_\mathrm{g} = 200\,\mu\mathrm{eV}` 
* :math:`\eta_\mathrm{pb} = 0.4`
