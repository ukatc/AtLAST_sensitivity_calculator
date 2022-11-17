![example workflow](https://github.com/ukatc/AtLAST_sensitivity_calculator/actions/workflows/backend-tests.yml/badge.svg)

:warning: **IMPORTANT: Do not merge this branch to main! This is a testing branch for benchmarking exercises only** :warning:

Some modifications to the calculations have been made to match other telescope efficiency parameterisations. These efficiencies do NOT need to be implemented in the final AtLAST sensitivity calculator and are only here to provide the closest match to the JCMT calculator online.

In progress software to calculate either:

1. required exposure time for a given sensitivity 

2. the reverse, the sensitivity for a given exposure time.


Documentation, including a ``User Guide`` can be found in the ``docs`` folder. To build the html version of the documentation, start from the main package directory and type ``cd docs; make html``. Read the documentation by pointing your browser at ``docs/build/html/index.html``.
