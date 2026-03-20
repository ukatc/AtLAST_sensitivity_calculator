Introduction
==========

The AtLAST Telescope Simulator example notebooks show users how to simulate
observations with AtLAST using the Sensitivity Calculator available in this 
repository

Using the Simulator
================================
The simulator comes in the form of a Jupyter lab notebook which can be downloaded
along with the sensitivity calculator here, and run on your local machine


Setting up your environment
===================================

The sensitvity calculator has a minimal set of required packages that it downloads
in order to run. In addition to those installed for the sensitivity calculator, to run
these simulation notebooks, you must also add the following python packages to your
conda environment

* matplotlib
* jupyter lab
* ipython
* reproject
* astroquery

They are not included in the python package to minimise the download size of the package
for those who are only interested in the sensitivity calculator itself.  To download
these packages, use either `pip install <package>` or `conda install <package>` in you
sensitivity calculator enviornment (if you downloaded the repo using pip or conda)
