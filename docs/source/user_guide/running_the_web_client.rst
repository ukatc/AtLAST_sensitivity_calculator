Installing and Running the Web Client
=====================================

The web client can be run on your computer in one of two ways - cloning
the AtLast Sensitivity Calculator and running the application directly, or
using a Docker image hosted on the GitHub Container Registry.

Instructions for each method are provided below.

.. note:: Please contact `Pamela Klaassen`_ if you require access to the repository.


.. note:: At a future release, the web client will be hosted on a publicly
    available server.

Running the web client directly
-------------------------------
You will first have to to clone the Sensitivity Calculator GitHub repository:

.. code-block:: bash

    $ git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git

The next step is to set up a developer conda environment using the `YAML` file
provided in the repository:

1. Navigate to the root directory of the repository (``AtLast_sensitivity_calculator``).

2. Create a conda environment:

.. code-block:: bash

   $ conda env create -f environment.yml


3. Activate the conda environment

.. code-block:: bash

   $ conda activate sens-calc

4. Start the web client application

.. code-block:: bash

   $ python -m web_client.main

5. Point your browser at http://127.0.0.1:8000/ . You should now see the Sensitivity Calculator web client.


Running the web client in a container
-------------------------------------

The web client can be run in a Docker container using an image hosted on the GitHub Container Registry.

Pulling the Docker image
^^^^^^^^^^^^^^^^^^^^^^^^

Follow the steps below to pull the Docker image.

1. Login to the GitHub Container Registry:

    .. code-block:: bash

        $ docker login ghcr.io

2. At the prompts, enter the username and Personal Access Token that you use to access the AtLast Sensitivity Calculator
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

        $ docker run --rm -d -p 8000:8000 --name atlast_sc ghcr.io/ukatc/atlast_sensitivity_calculator/atlast_sc_client:main

5. If the container runs successfully, point your browser at http://127.0.0.1:8000/.

   You should now see the Sensitivity Calculator web client.

.. _building-the-container:

Building and running the Docker container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Dockerfile is provided in the repository that can be used to build and run the web client application.
As part of the build process, the Dockerfile installs the Python application from the AtLast Sensitivity
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

        $ DOCKER_BUILDKIT=1 docker build -t atlast_sc_client:latest --secret id=git_secrets,src=secrets/.env .

2. Run the container with the command:

    .. code-block:: bash

        $ docker run --rm -d -p 8000:8000 --name atlast_sc_client atlast_sc_client:latest

3. Point your browser at http://127.0.0.1:8000/. You should now see the Sensitivity Calculator web client.


.. _Pamela Klaassen: pamela.klaassen@stfc.ac.uk