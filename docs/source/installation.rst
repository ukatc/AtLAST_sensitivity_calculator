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
#####################################

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
At present, the web client can only be run locally by first cloning the git repository:

.. code-block:: bash

    $ git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git

Running the web client
######################

The web client can be run directly in your development environment from the command line. Alternatively, it can be
run in a docker container. Instructions for each method are provided below.

Running the web client directly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You first need to set up your development environment as follows:

1. Create a conda environment:

.. code-block:: bash

   $ conda env create -f environment.yml


2. Activate the conda environment

.. code-block:: bash

   $ conda activate sens-calc

Once you have set up your environment, run the web client as follows:

1. Navigate to the `web_client` directory
2. Start a server with Flask (note: this may take a minute to load)

.. code-block:: bash

   $ flask run


3. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.


Running the web client in a container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Dockerfile is provided in the repository that can be used to build and run the web client application.
As part of the build process, the Dockerfile installs the python application from the AtLast Sensitivity
Calculator GitHub repository.

At present, the repository is private. You therefore need to provide your credentials as "secrets" to the
Docker build process. To do this:

1. Create a directory under `web_client` called `secrets`.
2. In the `secrets` directory, create a file called `.env` with the following content:

.. code-block:: bash

    GIT_USERNAME=<your username>
    GIT_PAT=<your Personal Access Token>


You can now build and run the Docker container as follows:

1. From the `web_client` directory, build the image with the command:

.. code-block:: bash

    $ DOCKER_BUILDKIT=1 docker build -t atlast_sc_client:latest --secret id=git_secrets,src=secrets/.env .

2. Run the container with the command:

.. code-block:: bash

    $ docker run --rm -d -p 5000:80 atlast_sc_client:latest -t atlast_sc_client

3. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.
