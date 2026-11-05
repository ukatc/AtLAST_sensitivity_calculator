Sensitivity Calculator Installation
===================================

The Sensitivity Calculator Python package can be installed from the `UKATC
AtLast Sensitivity Calculator GitHub repository <https://github.com/ukatc/AtLAST_sensitivity_calculator>`__.

.. _installing from git:

Installing the Python package from Git
--------------------------------------

Before you begin
^^^^^^^^^^^^^^^^

It is strongly recommended that you create a separate environment for your work using your
preferred environment management tool. We have tested the installation procedure with `conda <https://docs.conda.io/en/latest/>`__, and `mamba <https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html>`, although it may work with other tools. For instance, if you are using conda you can create an 
environment with:

.. code-block:: bash


   conda create -n atlast python=3.13 pip


Note that the calculator is tested to work with Python versions 3.10 to 3.13. We cannot ensure compatibility with other versions and so it is necessary to specify the version here.

After the environment is created, activate it with:

.. code-block:: bash

   conda activate atlast


If you want to install into an environment that you are already using, you can check your version of Python by
typing:

.. code-block:: bash

    python -V

Installing the sensitivity calculator Python package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have created and activated your environment, install the Sensitivity Calculator Python package from the
``main`` branch using pip:

.. code-block:: bash

    pip install git+https://github.com/ukatc/AtLAST_sensitivity_calculator.git


Extra packages for running the notebooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above installs the minimal set of packages required for the calculator to perform its calculations. However, extended functionality (i.e. plotting and using the included Jupyter Notebooks) requires additional packages to be installed. Having setup the proper conda environment for running the calculator (as described above), we recommend installing the following additional packages:

.. code-block:: bash

    conda install matplotlib jupyter reproject astroquery

The equivalent ``pip install`` command would work equally well in the conda environment.

*Known Errors:*

.. code-block:: bash 

   Channels:
    - defaults
   Platform: [...]
   Collecting package metadata (repodata.json): done
   Solving environment: failed
   
   PackagesNotFoundError: The following packages are not available from current channels:
   
     - [package_name/s]
   
   Current channels:
   
     - https://repo.anaconda.com/pkgs/main
     - https://repo.anaconda.com/pkgs/r


If you encounter the error above when using the above command then this means *conda-forge* is not set-up as one of your channels and you need to explicitly mention it:

.. code-block:: bash

    conda install -c conda-forge matplotlib jupyter reproject astroquery
