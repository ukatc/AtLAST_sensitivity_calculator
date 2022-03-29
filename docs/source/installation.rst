Installation
============

Eventually this calculator will be hosted on a server and made available publicly, however for the time being it can be downloaded from this repo and run locally.

To install the sensitivity calculator:

1. Clone this github repo: 

.. code-block:: bash

    $ git clone https://github.com/https://github.com/ukatc/AtLAST_sensitivity_calculator.git


To use the browser interface:
------------------------------

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

