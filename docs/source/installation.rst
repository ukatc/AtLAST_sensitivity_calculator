Installation
============

Eventually, the web client will be hosted on a publicly available server. The calculator will also be
available as a standalone python package, hosted on a publicly available server.

For the time being, both can be installed from the UKATC GitHub repository and run in your local environment.

Instructions are provided below.

Installing the Python package from Git
--------------------------------------

Before you begin
################

It is strongly recommended that you create a separate environment for your work using your
preferred environment management tool (e.g., `conda <https://docs.conda.io/en/latest/>`__,
`venv <https://realpython.com/python-virtual-environments-a-primer/>`__,
or `poetry <https://python-poetry.org/docs/>`__).

The sensitivity calculator python package requires Python >= 3.9. You can check your version of Python by
typing:

.. code-block:: bash

    $ python -V

If this returns ``2.x.x``, then try:

.. code-block:: bash

    $ python3 -V


Installing the sensitivity calculator
####################################

Once you have created and activated your environment, install the sensitivity python package using pip:

.. code-block:: bash

    $ pip install git+https://github.com/ukatc/AtLAST_sensitivity_calculator.git

This will install the package from the ``main`` branch of the repository.

You can install the package from a different branch by typing:

.. code-block:: bash

    $ pip install git+https://github.com/ukatc/AtLAST_sensitivity_calculator.git@<branch>

where ``<branch>`` is the name of the target branch.

Installing and running the web client
-------------------------------------

Setting up your environment
###########################

1. Clone the repository:

.. code-block:: bash

    $ git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git


2. Create a conda environment:

.. code-block:: bash

   $ conda env create -f environment.yml


3. Activate the conda environment

.. code-block:: bash

   $ conda activate sens-calc


Running the web client
######################

1. Navigate to the ``web_client`` directory
2. Start a server with Flask (note: this may take a minute to load)

.. code-block:: bash

   $ flask run


4. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.


