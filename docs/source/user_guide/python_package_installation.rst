Sensitivity Calculator Installation
===================================

The Sensitivity Calculator Python package can be installed from the `UKATC
AtLast Sensitivity Calculator GitHub repository <https://github.com/ukatc/AtLAST_sensitivity_calculator>`__.

Instructions are provided below.

.. _installing from git:

Installing the Python package from Git
--------------------------------------

Before you begin
^^^^^^^^^^^^^^^^

It is strongly recommended that you create a separate environment for your work using your
preferred environment management tool (e.g., `conda <https://docs.conda.io/en/latest/>`__,
`venv <https://realpython.com/python-virtual-environments-a-primer/>`__,
or `poetry <https://python-poetry.org/docs/>`__). For instance, if you are using conda you can create an 
environment with:

.. code-block:: bash


   conda create -n atlast python=3.12 pip


Note that the calculator is tested to work with Python versions 3.10 to 3.12. We cannot ensure compatibility with other versions and so it is necessary to specify the version here.

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

    conda install ipython matplotlib jupyter reproject astroquery

The equivalent ``pip install`` command would work equally well in the conda environment.
