Developing the application
==========================

Setting up your development environment
---------------------------------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git


2. Create a conda environment:

.. code-block:: bash

   conda env create -f environment.yml


3. Activate the conda environment

.. code-block:: bash

   conda activate sens-calc


The Python package
------------------
Building and deploying the Python package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The file ``pyproject.toml`` specifies build requirements and other information
such as package version, author information, etc. This file is used to build the
``atlast_ac`` package distribution archives.

To build the distribution archives, navigate to the root directory of the repository
and execute the following:

.. code-block:: bash

    python -m build

This will create a source distribution (``tar.gz`` file) and a built distribution
(``.whl`` file) in the ``dist`` directory.

TODO: complete

The ``buildpythonpackage`` target in the ``makefile`` performs this step.

.. note::

    FUTURE WORK: The ``atlast_sc`` package will be hosted on a publicly available server.
    Building and deploying the package should be automated using GitHub actions.

The web client
--------------
The web client can be run directly in your development environment from the command line. Alternatively, it can be
run in a docker container. Instructions for each method are provided below.

Running the web client directly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Ensure you have created and activated the conda environment as per the instructions above.
2. Run the web client with the following command from the main directory of the python package:

.. code-block:: bash

    python -m web_client.main

3. Point your browser at http://127.0.0.1:8000/ . You should now see the sensitivity calculator web client.

..
    .. _build-run-client-container:

    Building and running the web client container
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    A ``Dockerfile`` is provided in the repository that can be used to build and run
    the web client application in a docker container.

    .. note:: The ``Dockerfile`` uses the ``requirements.txt`` file in the ``web_client`` directory to install
        application dependencies in the container. This requirements file is not used by any other part of the
        application.

    As part of the build process, the Dockerfile installs the ``atlast_sc`` Python package from the AtLast Sensitivity
    Calculator GitHub repository.

    At present, the repository is private. You therefore need to provide your credentials as "secrets" to the
    Docker build process. To do this:

    1. Create a directory under ``web_client`` called ``secrets``.
    2. In the ``secrets`` directory, create a file called ``.env`` with the following content:

    .. code-block:: bash

       GIT_USERNAME=<your username>
       GIT_PAT=<your Personal Access Token>

    3. From the ``web_client`` directory, build the image with the command:

    .. code-block:: bash

        DOCKER_BUILDKIT=1 docker build -t atlast_sc_client:latest --secret id=git_secrets,src=secrets/.env .

    By default, the build process installs the ``atlast_sc`` package from the ``main`` branch. To install
    a version of the Python package from a different branch, execute the following:

    .. code-block:: bash

        DOCKER_BUILDKIT=1 docker build --build-arg BRANCH=<branch_name> -t atlast_sc_client:latest --secret id=git_secrets,src=secrets/.env .

    where ``<branch_name>`` is the name of the target branch.

    4. Run the container with the command:

    .. code-block:: bash

       docker run --rm -d -p 8000:8000 --name atlast_sc_client atlast_sc_client:latest


    5. Point your browser at http://127.0.0.1:8000/ . You should now see the sensitivity calculator web client.


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

    ..
        FUTURE WORK: The web client will be hosted on a publicly available server.
        Building and deploying the application should be automated using GitHub actions.


Adding a New Instrument
----------------------------------------
When an instrument needs to be added to the calculator, a couple of steps should be executed
within the *atlast_sc/instruments* directory. To be able to integrate the new instrument to the
existing calculator process, a YAML file with the name of the instrument, a Python module with 
the name of the instrument, and modifications to the configuration file should be made. Details 
of each of these steps are provided in the following sub-sections. Once the required files are 
created and modified, the new instrument should be visible on the CLI as well as the web UI and
will be used in calculations when the user input parameters correspond to the instrument's 
operational ranges. It should be noted that once the required files are in place, the developer 
should make sure to update the documentation to include the new instrument and its details, and
to provide an example of how to use it in calculations.

.. TODO::

    **ILGIN TO FOLLOW-UP**

    - what process does the user need to follow to have their instrument visible on the Oslo hosted site?

    I have re-opened ASC-114 to track this work


Creating the instrument YAML file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Firstly, a YAML file with the name of the instrument should be created in the 
sub-directory called *data*. It should include details of the instrument in the 
following format: 

.. code-block:: yaml

    name: "Example"
    allowed_ranges:
        observing_frequency:
            ranges: [(500.0-600.0),(700.0-800.0)]
            unit: GHz
        bandwidth: 
            ranges: [(10.9e4-1.8e8)]
            unit: Hz
    receiver_temperature: 
        values: [30.0,40.0]
        unit: K

Any other instrument specific parameter should be added following the same format. The
Default instrument YAML file could be taken as a template and the other instrument 
YAML files could be taken as example on how these files could be customised. 

Creating the instrument Python module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Secondly, a Python module should be created in the *classes* sub-directory with the
new instrument name. Following the example above, the name of the module file should 
be "Example.py" and it should include the following class format: 

.. code-block:: python 

    """
    Example instrument parameters
    """        
    class Example(Instrument):
        def __init__(self, data):
            super().__init__(data)

        ##################################
        # Instrument specific parameters #
        ##################################

        @property
        def custom_parameter(self):
            return self._custom_parameter

        @custom_parameter.setter
        def custom_parameter(self, value):
            self._custom_parameter = value

        ################################################
        # Additional instrument specific methods below #
        ################################################

        def custom_calculation_method(self):
            """
            Performs a custom calculation for the Example instrument. 
            This is just an example method and an example comment.
            """
            pass
        

For more detail on how to construct the module, the Default instrument Python module
could be taken as the base example. Below are different types of instrument categories
where the individual Python modules could be taken as an example on how a new instrument 
module in the same category could be customised:

    - Heterodynes (FINER, SEPIA, CHAI)
    - Continuum/LEKID (MUSCAT)
    - IFU/MKID (TIFUUN)

Modifying the configuration file to add the new instrument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Thirdly, a couple of lines should be modified in ``config.py`` where they are 
indicated within the configuration file with comments. In the initilisation 
method, a dictionary containing pointers to the new instrument's Python module 
and YAML file name should be added in similar format to the existing instruments. 
After creating the dictionary variable for the new instrument, it should be added 
to the ``available_instruments`` list.


Running the tests
-----------------
The ``atlast_sc`` package and FastAPI application tests are run using ``pytest``.
To run both test suites, navigate to the root directory of the repository and
execute the the ``pytest`` command.

To run tests and output a coverage report, execute:

.. code-block:: bash

    coverage run -m pytest
    coverage report -m

The targets ``testpackage`` and ``testwebclient`` in the repository ``makefile``
run tests with a coverage report for the ``atlast_sc`` package and FastAPI application respectively.


Generating the documentation
----------------------------



The project documentation is rendered in HTML using ``sphinx``. The source files
are located in the ``source`` directory under ``docs``.  readthedocs style documentation is
auto generated as described below, however the user can also re-create the documentation locally
following the commands below.


Local documentation generation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To build the HTML documentation:

1. Navigate to the ``docs`` directory.
2. Build the docs:

.. code-block:: bash

   make html

This will create the HTML and other resources in ``docs/build/``.

Open the file ``docs/build/html/index.html`` in your browser to view the built documentation.

Similarly, issuing the bash command ``make latexpdf`` will generate a PDF version of the documentation
as ``docs/latex/atlastsensitivitycalculator.pdf``.

..
    FUTURE WORK: The sphinx documentation will be hosted on a publicly available server.
    Building and deploying the documentation should be automated using GitHub actions.

Readthedocs
^^^^^^^^^^^

The project documentation is hosted at https://atlast-sensitivity-calculator.readthedocs.io/. This was set-up via the files

.. code-block:: bash

   .readthedocs.yaml
   docs/source/requirements.txt

The documentation is automatically updated with each new merge using webhooks.

Generating UML diagrams
-----------------------
UML diagrams for the ``atlast_sc`` package can be generated using ``pyreverse``. This is a set of
utilities for reverse engineering Python code that is integrated into ``pylint``.

This project uses `PlantUML <https://en.wikipedia.org/wiki/PlantUML>`__ to specify and
visualize UML diagrams.

To generate package and class ``puml`` files using ``pyreverse``, navigate to the ``atlast_sc`` directory
and execute the following:

.. code-block:: bash

    pyreverse -o puml -p atlast_sc .

This will generate ``puml`` files in the current directory, which you can edit as required.

.. note::

    The ``pyreverse`` tool is "imperfect". You will definitely want to edit the output.

See `here <https://pylint.readthedocs.io/en/latest/pyreverse.html>`__ for
information on how to use ``pyreverse``.

If you are using PyCharm IDE, a ``PlantUML`` plugin for rendering ``puml`` files is
available `here <https://plugins.jetbrains.com/plugin/7017-plantuml-integration>`__.

UML diagrams can be rendered in the sphinx documentation using the
``sphinxcontrib-plantuml`` extension. The ``code_docs`` directory contains a
number of examples of how to use the sphinx PlantUML extension.
