![example workflow](https://github.com/ukatc/AtLAST_sensitivity_calculator/actions/workflows/backend-tests.yml/badge.svg)


Background
==========

In progress software to calculate either:

1. required exposure time for a given sensitivity 

2. the reverse, the sensitivity for a given exposure time.

To be packaged as a standalone python package (WIP).

A simple web interface is included, follow installation instructions below.

Testing is incomplete but initial tests can be run using ``make test``.

The [``benchmarking``](https://github.com/ukatc/AtLAST_sensitivity_calculator/blob/benchmarking/README.md) branch is a work-in-progress to test the results of the calculator matching the input and setup to JCMT. This exercise is incomplete. As it includes changes to the underlying code (the efficiency calculation), it should **not** be merged with ``main``. 
After validation of the calculator results and before publication of this package, the ``benchmarking`` branch can be deleted.


Using The Sensitivity Calculater
================================
Eventually this calculator will be hosted on a server and made available publicly.

For the time being it can be installed or downloaded from this repository.

Documentation on how to install and use the Sensitivity Calculater can be found
in the [``installation guide``](docs/source/installation.rst).


Guide for Developers
====================
Setting up your environment
---------------------------

1. Clone the repository:

   ```
   $ git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git
   ```

2. Create a conda environment:

   ```
   $ conda env create -f environment.yml
   ```
   
3. Activate the conda environment

   ```
   $ conda activate sens-calc
   ```



Running the web client
----------------------
The web client can be run directly in your development environment from the command line. Alternatively, it can be
run in a docker container. Instructions for each method are provided below.

### Running the web client directly

1. Ensure you have created and activated the conda environment as per the instructions above.
2. Navigate to the `web_client` directory
3. Start a server with Flask (note: this may take a minute to load)

   ```
   $ flask run
   ```

4. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.


### Running the web client in a container

A Dockerfile is provided in the repository that can be used to build and run the web client application. 
As part of the build process, the Dockerfile installs the python application from the AtLast Sensitivity
Calculator GitHub repository.

At present, the repository is private. You therefore need to provide your credentials as "secrets" to the
Docker build process. To do this:

1. Create a directory under `web_client` called `secrets`.
2. In the `secrets` directory, create a file called `.env` with the following content:
   ```
   GIT_USERNAME=<your username>
   GIT_PAT=<your Personal Access Token>   
   ```

You can now build and run the Docker container as follows:
3. From the `web_client` directory, build the image with the command:
   ```
   $ DOCKER_BUILDKIT=1 docker build -t atlast_sc_client:latest --secret id=git_secrets,src=secrets/.env .
   ```
4. Run the container with the command:
   ```
   $ docker run --rm -d -p 5000:80 --name atlast_sc_client atlast_sc_client:latest
   ```

4. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator web client.

Generating the Documentation
-------------

To build the html version of the documentation:

1. Navigate to the [`docs`](docs/) directory.
2. Build the docs:

   ```
   $ make html
   ```

This will create the html and other resources in `docs/build/`.

Open the file `docs/build/html/index.html` in your browser to view the built documentation.