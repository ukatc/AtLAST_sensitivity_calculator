# MISTRAL Instrument Walkthrough

This doc shows how to use the AtLAST Sensitivity Calculator with the MISTRAL (MIllimieter Sardinia radio Telescope Receiver based on Array of Lumped elements KIDs), a KIDs camera observing in the W-band from the Sardinia Radio Telescope

## MISTRAL Specifications

- **Frequency Range**: 77-103 GHz
- **Type**: Lumped elements Kinetic Inductance Detectors (LEKIDs)
- **Purpose**: Wide area mapping

This walkthrough is based on the other AtLAST tutorial notebooks. 

This notebook calculates the sensitivity of MISTRAL based on preliminary
data acquired during the commissioning phase at the telescope. We
measure the Noise Equivalent Temperature (NET) of our detector array
with various atmospheric conditions, building scaling relation between
atmospheric opacity :math:`\tau` and the measured NET. We then convert
the NET to NEP using the following formula:

.. math::  NEP = 2 k_B \Delta\nu NET

we then estimate SEFD and system temperature following the same steps as
in the TIFUUN walkthrough:

.. math::  T_{sys} = \frac{NEP}{k_b \eta_{chip}\eta_{co}t\sqrt{2n_{pol}\Delta\nu}}

Since the NET is measured using the atmosphere at the SRT, that is an
extended source, we are already accounting for the efficiency of
detector array and cold optics, so we put these efficiencies to 1. We
set :math:`n_{pol}=1` (in this notation, it means averaging over the two
linear polarizations), as MISTRAL is not a polarimeter (yet).

Note that the NET estimates are **preliminary**. Also, given that this
calculator assumes AtLAST’s excellent atmosphere, the presented values
are a rather extreme extrapolation from SRT’s atmospheric conditions to
Atacama desert conditions. So, this notebook should not be used to plan
actual observations with MISTRAL.
