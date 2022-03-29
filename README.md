![example workflow](https://github.com/ukatc/AtLAST_sensitivity_calculator/actions/workflows/backend-tests.yml/badge.svg)


In progress software to calculate either:

1. required exposure time for a given sensitivity 

2. the reverse, the sensitivity for a given exposure time.

To be packaged as a standalone python package.

A web interface frontend is in development.

Installation
============

Eventually this calculator will be hosted on a server and made available publicly, however for the time being it can be downloaded from this repo and run locally.

To install the package the necessary steps are:

1. Clone this github repo: 

.. code-block:: bash

    $ git clone https://github.com/https://github.com/ukatc/AtLAST_sensitivity_calculator.git


2. Initialise your environment: this depends on what you use for environment management
    
    a) With poetry, create a poetry shell start a poetry shell in the directory of the repo:
    
    .. code-block::
        
        $ poetry shell
        Spawning shell within /home/user/.cache/pypoetry/virtualenvs/...
    

    b) With Conda:
    

    .. code-block:: bash
    
        $ conda env create -f environment.yml
        $ conda activate sens-calc
    

    c) With pip (not tested!):
    


    .. code-block:: bash
    
        $ pip install -r requirements.txt
    

3. Start a server with Flask:


.. code-block:: bash

    $ flask run
    * Serving Flask app 'sensitivity-calculator.py' (lazy loading)
    * Environment: development
    * Debug mode: on
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!


4. Point your browser at http://127.0.0.1:5000/. You should now see the sensitivity calculator browser interface!



Documentation, including a ``User Guide`` can be found in the ``docs`` folder. To build the html version of the documentation, start from the main package directory and type ``cd docs; make html``. Read the documentation by pointing your browser at ``docs/build/html/index.html``.