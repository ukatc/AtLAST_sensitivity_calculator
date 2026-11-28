import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import astropy.units as u
from atlast_sc import __version__
from atlast_sc.core.utils import DataHelper

from web_client.schemas import APIUserInput, InstrumentSelection, \
    ApplicableInstrumentsRequest, VelocityConversionRequest
import web_client.context_processors as cp
from web_client import utils, calculator


os.chdir(os.path.dirname(__file__))

app = FastAPI(
    title="AtLast Sensitivity Calculator",
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

version = f'v{__version__}'
paths = {
    'sensitivity': f'/{version}/sensitivity',
    'integration_time': f'/{version}/integration-time',
    'param_values_units': f'/{version}/param-values-units',
    'set_instrument': f'/{version}/set-instrument',
    'get_instrument': f'/{version}/get-instrument'
}

templates = Jinja2Templates(directory="templates",
                            context_processors=[cp.invalid_message_processor,
                                                cp.default_values_processor,
                                                cp.default_units_processor,
                                                cp.allowed_range_processor,
                                                cp.project_version,
                                                cp.api_version,
                                                ])

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def sensitivity_calculator(request: Request):
    from web_client.calculator import get_available_instruments
    instruments = get_available_instruments()
    return templates.TemplateResponse("sensitivity_calculator.html",
                                      {"request": request, "instruments": instruments})


@app.post(paths['sensitivity'])
async def sensitivity(api_user_input: APIUserInput):

    user_input = _unpack_api_user_input(api_user_input)

    # Convert special unit parameters to default unit equivalent
    user_input = utils.modify_user_input_with_converted_values(user_input)

    try:
        return calculator.do_calculation(
            user_input,
            "sensitivity",
            api_user_input.instrument_name,
            api_user_input.brightness_temperature,
        )
    except calculator.UserInputError as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.post(paths['integration_time'])
async def t_int(api_user_input: APIUserInput):

    user_input = _unpack_api_user_input(api_user_input)

    # Convert special unit parameters to default unit equivalent
    user_input = utils.modify_user_input_with_converted_values(user_input)

    try:
        return calculator.do_calculation(
            user_input, "integration_time", api_user_input.instrument_name
        )
    except calculator.UserInputError as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.get(paths['param_values_units'])
async def param_values_units():
    return JSONResponse(content=calculator.get_param_values_units())


@app.post(paths['set_instrument'] + '/convert-velocity')
async def velocity_to_frequency(req: VelocityConversionRequest):

    value, unit = DataHelper.convert_velocity_to_frequency(
        u.Quantity(req.obs_freq, u.GHz),
        u.Quantity(req.velocity, req.velocity_unit),
    )
    return JSONResponse(content={"value": value, "unit": str(unit)})


@app.post(paths['set_instrument'] + '/applicable-instruments')
async def get_applicable_instruments(req: ApplicableInstrumentsRequest):
    """
    Get current observing frequency and bandwidth values to determine
    a list of applicable instruments.

    :param req: JSON body with obs_freq, bandwidth and bandwidth_unit
    :return: list of applicable instrument names
    """
    obs_freq = req.obs_freq
    bandwidth_value = req.bandwidth
    bandwidth_unit = req.bandwidth_unit

    if bandwidth_unit in utils.special_units:
        bandwidth_value, bandwidth_unit = \
            DataHelper.convert_velocity_to_frequency(u.Quantity(obs_freq, str(u.GHz)),\
                                                     u.Quantity(bandwidth_value, bandwidth_unit))
        
    try:
        applicable_instruments = calculator.get_applicable_instruments(obs_freq, bandwidth_value, \
                                                                       bandwidth_unit)
        return JSONResponse(
            content=applicable_instruments
        )
    except Exception as e:
        # If there's an error, return Default
        return JSONResponse(
            content="Default"
        )

@app.get(paths['get_instrument'] + '/ranges')
async def get_instrument_ranges(instrument_name: str):
    """
    Get the observing frequency and bandwidth ranges for a given instrument.
    
    :param instrument_name: name of the instrument
    :return: frequency and bandwidth ranges
    """
    try:
        ranges = calculator.get_instrument_ranges(instrument_name)
        if ranges is None:
            ranges = calculator.get_instrument_ranges("Default")
        return JSONResponse(
            content=ranges
        )
    except Exception as e:
        # If there's an error, return Default ranges
        ranges = calculator.get_instrument_ranges("Default")
        return JSONResponse(
            content=ranges
        )



def _unpack_api_user_input(api_user_input):
    return {
        "t_int": api_user_input.t_int,
        "sensitivity": api_user_input.sensitivity,
        "bandwidth": api_user_input.bandwidth,
        "obs_freq": api_user_input.obs_freq,
        "n_pol": api_user_input.n_pol,
        "weather": api_user_input.weather,
        "elevation": api_user_input.elevation,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
