Python Package Installation Guide
=================================

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

   conda create -n atlast


Then activate the environment:

.. code-block:: bash

   conda activate atlast


If you want to install into an environment that you're already using, note that the Sensitivity Calculator 
package requires Python >= 3.10. You can check your version of Python by
typing:

.. code-block:: bash

    python -V

If this returns ``2.x.x``, then try:

.. code-block:: bash

    python3 -V


installing pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometimes pip in not installed with conda, and so the following extra step might be required to setup your environment properly
.. code-block:: bash

    conda install pip 

Installing the sensitivity calculator Python package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have created and activated your environment, install the Sensitivity Calculator Python package from the
``main`` branch using pip:

.. code-block:: bash

    pip install git+https://github.com/ukatc/AtLAST_sensitivity_calculator.git


Extra packages for running the notebooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The above installs all of the packages required for the calculator to run. 
The example notebooks require some extra packages that aren't installed by default. 
If you are running conda these can simply be installed with:

.. code-block:: bash

    conda install ipython matplotlib jupyter reproject astroquery


.. _Pamela Klaassen: pamela.klaassen@stfc.ac.uk
