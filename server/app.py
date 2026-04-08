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

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
