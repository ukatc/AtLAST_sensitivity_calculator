Python Package Installation Guide
=================================

The Sensitivity Calculator Python package can be installed from the UKATC
AtLast Sensitivity Calculator GitHub repository.

Instructions are provided below.

.. note:: Please contact `Pamela Klaassen`_ if you require access to the repository.


.. note:: At a future release, the web client will be hosted on a publicly
    available server. The Python package will also be installable from a
    publicly available repository.


.. _installing from git:

Installing the Python package from Git
--------------------------------------

Before you begin
^^^^^^^^^^^^^^^^

It is strongly recommended that you create a separate environment for your work using your
preferred environment management tool (e.g., `conda <https://docs.conda.io/en/latest/>`__,
`venv <https://realpython.com/python-virtual-environments-a-primer/>`__,
or `poetry <https://python-poetry.org/docs/>`__).

The Sensitivity Calculator package requires Python >= 3.10. You can check your version of Python by
typing:

.. code-block:: bash

    $ python -V

If this returns ``2.x.x``, then try:

.. code-block:: bash

    $ python3 -V


Installing the sensitivity calculator Python package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have created and activated your environment, install the Sensitivity Calculator Python package from the
``main`` branch using pip:

.. code-block:: bash

    $ pip install git+https://<GIT_USERNAME>:<GIT_PAT>@github.com/ukatc/AtLAST_sensitivity_calculator.git

where ``<GIT_USERNAME>`` and ``<GIT_PAT>`` are the username and personal access token that you use to access the AtLast
Sensitivity Calculator GitHub repository.

You can install the package from a different branch by typing:

.. code-block:: bash

    $ pip install git+https://<GIT_USERNAME>:<GIT_PAT>@github.com/ukatc/AtLAST_sensitivity_calculator.git@<branch>

where ``<branch>`` is the name of the target branch.


.. _Pamela Klaassen: pamela.klaassen@stfc.ac.uk
