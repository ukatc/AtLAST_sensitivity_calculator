TIFUUN system temperature
=========================

Terahertz IFU with Universal Nanotechnology TIFUUN is being built for the ASTE Observatory. TIFUUN is a KID (Kinetic Inductance Detector) instrument. It covers the frequency range between 90 and 360 GHz. It is set-up to cover channel spacings from 180 MHz to 10 GHz.  (See `Rybak et al. 2024 <https://zenodo.org/records/12202439>`__ for more details.)

The system temperature is calculated as:

.. math::
    T_{sys} = \frac{\mathrm{NEP}}{k\,\eta_\mathrm{chip}\,\eta_\mathrm{co}\,\eta_\mathrm{eff}\,\mathfrak{t}\,\sqrt{2n_\mathrm{pol}\,\Delta\nu} }

where

* :math:`\mathrm{NEP}` is the Noise Equivalent Power
* :math:`\eta_{eff}` is the forward efficiency
* :math:`\eta_{chip}` is the chip optical efficiency
* :math:`\eta_{co}` is the cold optics optical efficiency
* :math:`\mathfrak{t}` is the atmospheric transmittance, defined as :math:`\mathfrak{t} = \textrm{exp}^{(-\tau_{atm})}.`

The Noise Equivalent Power is calculated as:

.. math::
    \mathrm{NEP} = \sqrt{2\,P_\mathrm{KID}\,h\,\nu+2\,P_\mathrm{KID}^2/(n_\mathrm{pol}\Delta \nu)+4\,\Delta_\mathrm{g}\,P_\mathrm{KID}/\eta_{pb}}

where

* :math:`P_\mathrm{KID}` is the power received by the KID
* :math:`\Delta_\mathrm{g}` is the gap energy of the superconductor
* :math:`\eta_{pb}` is the pair-breaking efficiency.

The power received by the KID (:math:`P_\mathrm{KID}`) is dependent on the power spectral density (:math:`PSD_\mathrm{KID}`) and calculated as:

.. math::
    P_\mathrm{KID}(\nu_\mathrm{0}) = \int^{\nu_\mathrm{max}}_{\nu_\mathrm{min}} PSD_\mathrm{KID}(\nu)\: d\nu \sim PSD_\mathrm{KID}(\nu_\mathrm{0}) \Delta \nu
    
    PSD_\mathrm{KID}(\nu) = & \eta_\mathrm{chip}(1-\eta_\mathrm{co})\cdot h\nu\cdot O(\nu, T_\mathrm{co})\\
                            &+ \eta_\mathrm{chip}\,\eta_\mathrm{co}(1-\eta_\mathrm{eff})\cdot h\nu\cdot O(\nu, T_\mathrm{amb})\\
                            &+ \eta_\mathrm{chip}\,\eta_\mathrm{co}\,\eta_\mathrm{eff}(1-t_\mathrm{r})\cdot h\nu\cdot O(\nu, T_\mathrm{atm})\\
                            &+ \eta_\mathrm{chip}\,\eta_\mathrm{co}\,\eta_\mathrm{eff}\,t_\mathrm{r}\cdot h\nu\cdot O(\nu, T_\mathrm{cmb})

where 

* :math:`T_{co}` is the temperature of the cold optics
* :math:`T_{atm}` is the atmospheric temperature calculated from the model grid described in :doc:`Weather Calculations <weather>`
* :math:`T_{cmb}` is the temperature of the cosmic microwave background
* :math:`T_{amb}` is the ambient temperature.

Here, :math:`O(\nu, T)` is the Bose-Einstein photon-occupation number

.. math::
    O(\nu, T) = \frac{1}{\exp(h\nu/kT)-1}.

For TIFUUN, the constants are expected to have the following values (based on information provided by the TIFUUN team):

* :math:`\eta_{chip} = 0.26`
* :math:`\eta_{co} = 0.65` 
* :math:`\Delta_\mathrm{g} = 188\,\mu\mathrm{eV}` 
* :math:`\eta_{pb} = 0.4`
* :math:`T_{co} = 4\,\mathrm{K}`