import logging

from flask import Flask, render_template, request, jsonify

import astropy.units as u
from atlast_sc.calculator import Calculator

app = Flask(__name__)

handler = logging.StreamHandler()
app.logger.addHandler(handler)
app.logger.propagate = False
app.logger.level = logging.DEBUG


@app.route('/', methods=('GET', 'POST'))
def template():
    return render_template('SensitivityCalculator.html')


@app.route('/hello')
def hello():
    return "Hello2 World"


@app.route('/documentation')
def docs():
    return "To build the html version of the documentation, start from the main package directory and type ``cd docs; make html'. Read the documentation by pointing your browser at ``{}/docs/build/html/index.html".format(app.root_path)

@app.route('/v1/sensitivity')
def sensitivity():
    app.logger.debug('sensitivity1')
    print('received request', request)
    inputs = {}
    inputs['bandwidth'] = {'value': float(request.args.get('bandwidth')), 'unit':'GHz'}
    inputs['obs_freq'] = {'value': float(request.args.get('obs_freq')), 'unit':'GHz'}
    inputs['n_pol'] = {'value': int(request.args.get('npol')), 'unit':'none'}
    inputs['weather'] = {'value': float(request.args.get('pwv')), 'unit': 'none'}
    inputs['elevation'] = {'value': float(request.args.get('elevation')), 'unit': 'deg'}
    # inputs['g'] = {'value': float(request.args.get('g')), 'unit': 'none'}
    # inputs['surface_rms'] = {'value': 25, 'unit': 'micron'}
    # inputs['dish_radius'] = {'value': 25, 'unit': 'm'}
    # inputs['T_amb'] = {'value': float(request.args.get('Tamb')), 'unit': 'K'}
    # inputs['T_rx'] = {'value': float(request.args.get('Trx')), 'unit': 'K'}
    # inputs['eta_eff'] = {'value': float(request.args.get('eta_eff')), 'unit': 'none'}
    # inputs['eta_ill'] = {'value': float(request.args.get('eta_ill')), 'unit': 'none'}
    # inputs['eta_q'] = {'value': float(request.args.get('eta_g')), 'unit': 'none'}

    if 'integration_time' in request.args:
        inputs['t_int'] = {'value': float(request.args.get('integration_time')), 'unit':'s'}
    if 'sensitivity' in request.args:
        inputs['sensitivity'] = {'value': float(request.args.get('sensitivity')), 'unit':'mJy'}

    app.logger.debug(inputs)

    # config = Config(inputs)
    calculator = Calculator(inputs)

    result_dict = {}
    # TODO: the requirement that exactly one of sensitivity and int time should have a value is causing and error.
    #       Remove this requirement. It's not adding anything useful.
    if 'integration_time' in request.args:
        result = calculator.calculate_sensitivity(calculator.t_int).to(u.mJy)
        app.logger.debug('calculator.calculate_sensitivity')
        app.logger.debug(result)
        result_dict["sensitivity"] = f"{result:0.03f}"
    elif 'sensitivity' in request.args:
        result = calculator.calculate_t_integration(calculator.sensitivity)
        app.logger.debug('calculator.calculate_t_integration')
        app.logger.debug(result)
        result_dict["integration_time"] = f"{result:0.03f}"

    app.logger.debug(result_dict)

    result = jsonify(result_dict)
    return result
