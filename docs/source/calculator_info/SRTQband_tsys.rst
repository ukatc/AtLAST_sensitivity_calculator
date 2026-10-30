SRTQBand system temperature
========================

THE SRTQband is the 19-feed receiver installed on the Sardinia Radio Telescope. It was developed under the project 

*The Enhancement of the Sardinia Radio Telescope
for the Study of the Universe at High Radio Frequen
cies*, financially supported by the *Programma
Operativo Nazionale del Italian Ministry of Education,
Universities and Research Ricerca e Innovazione
2014–2020 proposal  PIR01_00010*.  (`SRT QBand  <https://sites.google.com/a/inaf.it/pon-srt/home/o-r-2>`__) 


The receiver works from 33 to 50 GHz. It has a receiver temperature between 16 K and 23 K. The spectral channel frequency spacing depends on the backend. For the SKARAB backend varies from 1.5 GHz down to 22.8 KHz. (See `Melis et al. 2022 <https://www.worldscientific.com/doi/epdf/10.1142/S2251171724500089>`__ for more details about the backend.)

Here in the AtLAST sensitivity calculator, we use it as an exemplar of a heterodyne instrument capable of working at these frequencies.

In this module, we calculate the system temperature used in the overall :doc:`sensitivity equation <sensitivity>`. For a heterodyne  like system, the system temperature is calculated as:

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

The :math:`T_{rx}` is in the range between 16 K and 23 K over the whole receiver bandwidth, with lower values at the lowest frequencies. 
These values are used in the :math:`T_{sys}` equation above, which is in turn used to calculate the System Equivalent Flux Density used in the overall sensitivity (or integration time) calculation.


