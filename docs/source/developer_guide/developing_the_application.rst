Developing the application
==========================

Setting up your development environment
---------------------------------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/ukatc/AtLAST_sensitivity_calculator.git


2. Create a conda environment:

.. code-block:: bash

   conda env create -f AtLAST_sensitivity_calculator/environment.yml


3. Activate the conda environment

.. code-block:: bash

   conda activate sens-calc


The Python Package
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

The ``buildpythonpackage`` target in the ``makefile`` performs this step.

.. note::

    FUTURE WORK: The ``atlast_sc`` package will be hosted on a publicly available server.
    Building and deploying the package should be automated using GitHub actions.

The Web Client
--------------
The web client can be run directly in your development environment from the command line.

Running the web client locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Ensure you have created and activated the conda environment as per the instructions above.
2. Run the web client with the following command from the main directory of the python package:

.. code-block:: bash

    python -m web_client.main

3. Point your browser at http://127.0.0.1:8000/ . You should now see the sensitivity calculator web client.


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
visualize UML diagrams. UML diagrams can be rendered in the sphinx documentation using the
``sphinxcontrib-plantuml`` extension. The ``code_docs`` directory contains a
number of examples of how to use the sphinx PlantUML extension.

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


