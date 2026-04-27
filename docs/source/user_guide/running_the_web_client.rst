Running the Web Client
======================

The web client can be accessed from https://senscalc.atlast.uio.no/.

The web client can also be run on your computer in one of two ways - cloning
the AtLast Sensitivity Calculator and running the application directly, or
using a Docker image hosted on the GitHub Container Registry.

Instructions for each method are provided below.


Running the web client directly
-------------------------------
To run the web client directly in your local development environment, you
will first have to to clone the Sensitivity Calculator GitHub repository:

.. code-block:: bash

    git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git

The next step is to set up a developer conda environment using the `YAML` file
provided in the repository:

1. Navigate to the root directory of the repository (``AtLast_sensitivity_calculator``).

2. Create a conda environment:

.. code-block:: bash

   conda env create -f environment.yml


3. Activate the conda environment

.. code-block:: bash

   conda activate sens-calc

4. Start the web client application

.. code-block:: bash

   python -m web_client.main

5. Point your browser at http://127.0.0.1:8000/ . You should now see the Sensitivity Calculator web client.


