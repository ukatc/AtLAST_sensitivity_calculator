from fastapi import FastAPI, HTTPException
from schemas import APIUserInput
import crud

app = FastAPI()


@app.post("/v1/sensitivity")
async def sensitivity(api_user_input: APIUserInput):

    user_input = _unpack_api_user_input(api_user_input)

    try:
        return crud.do_calculation(user_input, "sensitivity")
    except crud.UserInputError as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.post("/v1/integration-time")
async def t_int(api_user_input: APIUserInput):

    user_input = _unpack_api_user_input(api_user_input)

    try:
        return crud.do_calculation(user_input, "integration_time")
    except crud.UserInputError as e:
        raise HTTPException(status_code=400, detail=e.message)


@app.get("/v1/param-values-units")
async def param_values_units():
    return crud.get_param_values_units()


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
