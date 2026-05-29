Quickstart guide
================

This guide demonstrates how to install the calculator as a python package and run it to get a quick result. 

Installing the Python package from Git
--------------------------------------

We recommend creating a fresh environment before installing using pip. Here we assume conda as the environment manager, although the code will also install into environments created using other environment managers.

.. code-block:: bash

   conda create -n atlast python=3.12 pip # create a fresh environment
   conda activate atlast # activate the environment
   pip install git+https://github.com/ukatc/AtLAST_sensitivity_calculator.git # install from Github

Calculating a sensitivity / integration time
--------------------------------------------

Now start ``python`` and run the following to calculate your sensitivity / integration time.

.. code-block:: python

    from atlast_sc.calculator import Calculator # import the calculator package
    import astropy.units as u # we'll need this to define the units of the user input parameters

    calculator = Calculator() # initialise the calculator object
    calculator.user_input.show() # check the default user input parameters
    calculator.user_input.obs_freq = 650*u.GHz # choose desired frequency
    calculator.user_input.bandwidth = 1*u.MHz # choose desired bandwidth / spectral resolution
    calculator.user_input.t_int = 1*u.h # set the integration time

    sensitivity = calculator.calculate_sensitivity() # calculate sensitivity
    print(sensitivity) # print the result

    calculator.user_input.sensitivity = 300*u.mJy # alternatively, set the sensitivity
    time = calculator.calculate_t_integration() # and calculate the integration time
    print(time) # print the result



