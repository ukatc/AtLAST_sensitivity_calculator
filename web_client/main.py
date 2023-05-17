import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from schemas import APIUserInput
import utils
import crud
import context_processors as cp


app = FastAPI(
    title="AtLast Sensitivity Calculator",
    version=utils.VERSION,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

version = f'v{utils.version_num_for_url()}'
paths = {
    'sensitivity': f'/{version}/sensitivity',
    'integration_time': f'/{version}/integration-time',
    'param_values_units': f'/{version}/param-values-units'
}

templates = Jinja2Templates(directory="templates",
                            context_processors=[cp.invalid_message_processor,
                                                cp.default_values_processor,
                                                cp.default_units_processor,
                                                cp.allowed_range_processor,
                                                cp.api_version,
                                                ])

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/scripts", StaticFiles(directory="scripts"), name="scripts")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def sensitivity_calculator(request: Request):
    return templates.TemplateResponse("sensitivity_calculator.html",
                                      {"request": request,
                                       "params_vals_units":
                                           crud.get_param_values_units()})


@app.post(paths['sensitivity'])
async def sensitivity(api_user_input: APIUserInput):

    user_input = _unpack_api_user_input(api_user_input)

    try:
        return crud.do_calculation(user_input, "sensitivity")
    except crud.UserInputError as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.post(paths['integration_time'])
async def t_int(api_user_input: APIUserInput):

    user_input = _unpack_api_user_input(api_user_input)

    try:
        return crud.do_calculation(user_input, "integration_time")
    except crud.UserInputError as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.get(paths['param_values_units'])
async def param_values_units():
    return JSONResponse(content=crud.get_param_values_units())


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
