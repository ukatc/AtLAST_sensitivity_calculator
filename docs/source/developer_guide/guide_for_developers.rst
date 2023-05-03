Guide for Developers
====================

Setting up your development environment
---------------------------------------

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
The web client can be run directly in your development environment from the command line. Alternatively, it can be
run in a docker container. Instructions for each method are provided below.

Running the web client directly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Ensure you have created and activated the conda environment as per the instructions above.
2. Navigate to the ``web_client`` directory
3. Run the web client with the following command:

.. code-block:: bash

    $ python -m main

4. Point your browser at http://127.0.0.1:8000/ . You should now see the sensitivity calculator web client.


Running the web client in a container
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
3. From the ``web_client`` directory, build the image with the command:

.. code-block:: bash

    $ DOCKER_BUILDKIT=1 docker build -t atlast_sc_client:latest --secret id=git_secrets,src=secrets/.env .

4. Run the container with the command:

.. code-block:: bash

   $ docker run --rm -d -p 8000:8000 --name atlast_sc_client atlast_sc_client:latest


5. Point your browser at http://127.0.0.1:8000/ . You should now see the sensitivity calculator web client.

Running the tests
-----------------
TODO: complete the docs.

Building and deploying the application
--------------------------------------
Building the Python package
^^^^^^^^^^^^^^^^^^^^^^^^^^^

TODO: complete the docs.

Building and deploying the web client container image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The web client container image can be built and pushed to the GitHub Container Registry using the ``makefile`` in the
root directory of the repository.

To do this, you will first have to create a GitHub Personal Access Token with the
appropriate scopes. See `here <https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic>`__
for more information.

Next, add the following two variables to your local ``.env`` file (in the ``web_client/secrets`` directory):

.. code-block:: bash

   GIT_CR_PAT=<YOUR GITHUB PAT>
   GIT_CR_REPO=ghcr.io/ukatc/atlast_sensitivity_calculator/atlast_sc_client


The are two targets in the ``makefile`` for building and pushing the container image:

* ``buildwebclientimage``: This builds the image and tags it with the name of your current git branch (e.g., ``main``). The
  current branch name is also passed as an argument to the build process. This is then used to install the Python package
  in the container *from that branch*. Note - this means that your branch must exist in the remote repository, and be
  up-to-date.
* ``pushwebclientimage``: This first executes the ``buildwebclientimage`` target, then pushes the built image to the GitHub
  Container Registry.



Generating the documentation
----------------------------

To build the html version of the documentation:

1. Navigate to the ``docs`` directory.
2. Build the docs:

.. code-block:: bash

   $ make html

This will create the html and other resources in ``docs/build/``.

Open the file ``docs/build/html/index.html`` in your browser to view the built documentation.