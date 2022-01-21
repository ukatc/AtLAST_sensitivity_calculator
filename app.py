import logging

from flask import Flask, render_template, request, jsonify

import astropy.units as u
from astropy.coordinates import SkyCoord
from configs.config import Config
from backend.sensitivity import Sensitivity


app = Flask(__name__)

handler = logging.StreamHandler()
app.logger.addHandler(handler)
app.logger.propagate = False
app.logger.level = logging.DEBUG

@app.route('/')
def template():
    return render_template('SensitivityCalculator.html')

@app.route('/hello')
def hello():
    return "Hello2 World"

@app.route('/v1/sensitivity')
def sensitivity():
    app.logger.debug('sensitivity1')

    ra = request.args.get("right_asc")
    dec = request.args.get("dec")
    app.logger.debug('right_asc {ra}'.format(ra=ra))
    app.logger.debug('dec {dec}'.format(dec=dec))
    frame = "icrs"

    target = SkyCoord(
        ra, dec, frame=frame, unit=(u.hourangle, u.deg)
    )

    inputs = {}
    inputs['t_int'] = {'value':10.1, 'unit':'s'}
#    inputs['sensitivity'] = {'value':1e-6, 'unit':'mJy'}
    inputs['bandwidth'] = {'value':1e6, 'unit':'Hz'}
    inputs['obs_freq'] = {'value':100e9, 'unit':'Hz'}
    inputs['n_pol'] = {'value':2, 'unit':'none'}
    inputs['weather'] = {'value': 50, 'unit': 'none'}
    inputs['elevation'] = {'value': 30, 'unit': 'deg'}
    inputs['g'] = {'value': 1.0, 'unit': 'none'}
    inputs['surface_rms'] = {'value': 25, 'unit': 'micron'}
    inputs['dish_radius'] = {'value': 25, 'unit': 'm'}
    inputs['T_amb'] = {'value': 270, 'unit': 'K'}
    inputs['T_rx'] = {'value': 50, 'unit': 'K'}
    inputs['eta_eff'] = {'value': 0.8, 'unit': 'none'}
    inputs['eta_ill'] = {'value': 0.63, 'unit': 'none'}
    inputs['eta_q'] = {'value': 0.96, 'unit': 'none'}

    app.logger.debug(inputs)

    config = Config(inputs)
    calculator = Sensitivity(config)

    if config.t_int.value and not config.sensitivity.value: 
        result = calculator.sensitivity(config.t_int).to(u.mJy) 
        app.logger.debug('calculator.sensitivity')
        app.logger.debug(result)

    result_dict = {}
    result_dict["sensitivity"] = f"{result:0.03f}"
    app.logger.debug(result_dict)

    result = jsonify(result_dict)
    return result

