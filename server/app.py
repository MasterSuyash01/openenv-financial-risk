from fastapi import FastAPI
from my_env.env import FinancialEnv
from my_env.models import Action

app = FastAPI()
env = FinancialEnv()


@app.post("/reset")
async def reset():
    result = await env.reset()
    return result.dict()


@app.post("/step")
async def step(action: Action):
    result = await env.step(action)
    return result.dict()