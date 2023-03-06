Installation Guide
==================

Eventually, the web client will be hosted on a publicly available server. The calculator will also be
available as a standalone python package, hosted on a publicly available server.

For the time being, both can be installed from the UKATC AtLast Sensitivity Calculator GitHub repository and
run in your local environment.

Please contact `Pamela Klaassen`_ if you require access to the repository.

Instructions are provided below.

.. _installing from git:

Installing the Python package from Git
--------------------------------------

Before you begin
^^^^^^^^^^^^^^^^

It is strongly recommended that you create a separate environment for your work using your
preferred environment management tool (e.g., `conda <https://docs.conda.io/en/latest/>`__,
`venv <https://realpython.com/python-virtual-environments-a-primer/>`__,
or `poetry <https://python-poetry.org/docs/>`__).

The sensitivity calculator python package requires Python >= 3.10. You can check your version of Python by
typing:

.. code-block:: bash

    $ python -V

If this returns ``2.x.x``, then try:

.. code-block:: bash

    $ python3 -V


Installing the sensitivity calculator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have created and activated your environment, install the Sensitivity Calculator python package from the
``main`` branch using pip:

.. code-block:: bash

    $ pip install git+https://<GIT_USERNAME>:<GIT_PAT>@github.com/ukatc/AtLAST_sensitivity_calculator.git

where ``<GIT_USERNAME>`` and ``<GIT_PAT>`` are the username and personal access token that you use to access the AtLast
Sensitivity Calculator GitHub repository.

You can install the package from a different branch by typing:

.. code-block:: bash

    $ pip install git+https://<GIT_USERNAME>:<GIT_PAT>@github.com/ukatc/AtLAST_sensitivity_calculator.git@<branch>

where ``<branch>`` is the name of the target branch.

Installing and running the web client
-------------------------------------
At present, the web client can only be run locally, but will eventually be hosted on a publicly available server.

The web client can be run directly in your development environment from the command line. Alternatively, it can be
run in a docker container. Instructions for each method are provided below.

Running the web client directly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
First, you need to clone the Sensitivity Calculator GitHub repository:

.. code-block:: bash

    $ git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git

Next, set up your development environment as follows:

1. Create a conda environment:

.. code-block:: bash

   $ conda env create -f environment.yml


2. Activate the conda environment

.. code-block:: bash

   $ conda activate sens-calc

Once you have set up your environment, run the web client as follows:

1. Navigate to the ``web_client`` directory
2. Start a server with Flask (note: this may take a minute to load)

.. code-block:: bash

   $ flask run


3. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.


Running the web client in a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pulling the Docker image
++++++++++++++++++++++++

A Docker container image is provided for running the web client. This can be pulled from the GitHub Container
Registry as follows:

1. Login to the registry:

.. code-block:: bash

    $ docker login ghcr.io

2. At the prompts, enter the username and Personal Accss Token that you use to access the AtLast Sensitivity Calculator
repository.

3. Pull the image:

.. code-block:: bash

    $ docker pull ghcr.io/ukatc/atlast_sensitivity_calculator/atlast_sc_client:main

You may see the following error at this point:

``error pulling image configuration: Get "https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:...": remote error: tls: handshake failure``

There a number of possible causes of this error. See `here <https://aboutssl.org/fix-ssl-tls-handshake-failed-error/>`__ for more information.

If you are connected to a VPN, try disconnecting, if possible.

If you are unable to find a workaround for this error, you can build and run the container following the steps
described in the section :ref:`building-the-container`.


4. If the image was pulled successfully, run the container:

.. code-block:: bash

    $ docker run --rm -d -p 5000:80 --name atlast_sc ghcr.io/ukatc/atlast_sensitivity_calculator/atlast_sc_client:main

5. If the container runs successfully, point your browser at http://127.0.0.1:5000/.

You should now see the sensitivity calculator web client.

.. _building-the-container:

Building and running the Docker container
+++++++++++++++++++++++++++++++++++++++++

A Dockerfile is provided in the repository that can be used to build and run the web client application.
As part of the build process, the Dockerfile installs the python application from the AtLast Sensitivity
Calculator GitHub repository.

At present, the repository is private. You therefore need to provide your credentials as "secrets" to the
Docker build process. To do this:

1. Create a directory under ``web_client`` called ``secrets``.
2. In the ``secrets`` directory, create a file called ``.env`` with the following content:

.. code-block:: bash

    GIT_USERNAME=<your username>
    GIT_PAT=<your Personal Access Token>


You can now build and run the Docker container as follows:

1. From the ``web_client`` directory, build the image with the command:

.. code-block:: bash

    $ DOCKER_BUILDKIT=1 docker build -t atlast_sc_client:main --secret id=git_secrets,src=secrets/.env .

2. Run the container with the command:

.. code-block:: bash

    $ docker run --rm -d -p 5000:80 --name atlast_sc_client atlast_sc_client:main

3. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.


.. _Pamela Klaassen: pamela.klaassen@stfc.ac.uk
