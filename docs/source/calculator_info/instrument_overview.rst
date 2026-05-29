Instrument Overview
===================

At the current stage of development, we are a long way from knowing any precise details of the instrument suite available on AtLAST. Nevertheless, we expect to see a variety of spectrometers, IFUs and continuum cameras. As our default instrument, we use a generic receiver with a noise equivalent temperature of :math:`5h\nu/k`.

To go beyond this, in order to approximate the future instrumentation available on AtLAST, we have worked with instrument teams that are designing the latest instruments for single-dish sub-mm and mm telescopes. This is in no way to suggest that these particular instruments will be available on AtLAST, but by representing these in our calculator, we aim to provide examples of what could achieved by using the most cutting-edge instruments on a telescope with a 50m primary mirror.

.. csv-table::
    :header: "Name", "Telescope", "Project page"
    :widths: 6,6,30

    :doc:`CHAI <chai_tsys>`, CCAT, https://www.ccatobservatory.org/chai/
    :doc:`FINER <finer_tsys>`, LMT, https://finerreceiver.github.io/
    :doc:`MUSCAT <muscat_tsys>`, LMT, https://muscat-docs.astro.cf.ac.uk/
    :doc:`SEPIA <sepia_tsys>`, APEX, https://www.apex-telescope.org/ns/observing/the-telescope/instruments/sepia/sepia345/
    :doc:`TIFUUN <tifuun_tsys>`, ASTE,

Observing frequency and channel bandwidth ranges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Each instrument has a specified range of frequencies, :math:`\nu`, and bandwidths, :math:`\Delta\nu`, (note by bandwidth here we mean either the continuum bandwidth or the desired spectral resolution) as shown in the table and plot below. The calculator will select the appropriate instrument based on the user input frequency and bandwidth, with the default heterodyne being selected for any regions of parameter space not covered by the following instruments. For cases where two or more instruments overlap in parameter space, an arbitrary instrument will be selected. This can then be changed by the user as described in the :ref:`user guide <section_instrument_selection>`.

+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| Name   | Min :math:`\nu` (GHz) | Max :math:`\nu` (GHz) | Min :math:`\Delta\nu`      | Max :math:`\Delta\nu`      |
+========+=======================+=======================+============================+============================+
| High resolution spectrometers                                                                                    |
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| FINER  |                   120 |                   210 |                     88 kHz |                    180 MHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| FINER  |                   210 |                   360 |                     88 kHz |                    180 MHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| SEPIA  |                   272 |                   376 |                   62.5 kHz |                    180 MHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| CHAI   |                   460 |                   500 |                     61 kHz |                      4 GHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| CHAI   |                   780 |                   820 |                     61 kHz |                      4 GHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| Wide band spectrometers                                                                                          |
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| TIFUUN |                    90 |                   360 |                    180 MHz |                     10 GHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| Continuum cameras                                                                                                |
+--------+-----------------------+-----------------------+----------------------------+----------------------------+
| MUSCAT |                   250 |                   300 |                     10 GHz |                     80 GHz | 
+--------+-----------------------+-----------------------+----------------------------+----------------------------+

.. image:: imgs/bandvsfreq_extended.png
    :alt: Bandwidth vs. frequency parameter space of the supported instruments
    :align: center
    :width: 500px

System temperatures
^^^^^^^^^^^^^^^^^^^
Each instrument has a module to calculate its system temperature :math:`T_\mathrm{sys}` that fits into the following equation for the System Equivalent Flux Density that is required for the final :doc:`sensitivity calculation <sensitivity>`:

.. math::
    SEFD = \frac{2kT_\mathrm{sys}}{\eta_\mathrm{A}A_\mathrm{g}}

where

* :math:`k` is the Boltzmann constant
* :math:`\eta_\mathrm{A}` is the dish efficiency
* :math:`A_\mathrm{g}` is the geometric dish area

The system temperature is calculated based on the user input parameters as well as parameters for the telescope, environment and the instrument itself. More information on the instruments and a detailed explanation of the equations used to calculate their system temperatures can be found in the following pages.

.. toctree::
    :maxdepth: 2
    
    chai_tsys
    finer_tsys
    sepia_tsys
    muscat_tsys
    tifuun_tsys