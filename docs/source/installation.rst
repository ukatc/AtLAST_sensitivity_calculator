Installation
============

Eventually this calculator will be hosted on a server and made available publicly, however for the time
being it can be downloaded from the GitHub repo and run locally following the steps below.

Eventually this calculator will be hosted on a server and made available publicly, however for the time being it can be downloaded from this repo and run locally.

Setting up your environment
---------------------------

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
----------------------

1. Navigate to the `web_client` directory
2. Start a server with Flask (note: this may take a minute to load)

.. code-block:: bash

   $ flask run


4. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client!


