from fastapi import FastAPI, Request
from ambulance_env import AmbulanceDispatchEnv
import uvicorn

app = FastAPI()
env = AmbulanceDispatchEnv()

@app.get("/")
def ping():
    # Hackathon spec: must return 200
    return {"status": "ok"}

@app.post("/reset")
async def reset(request: Request):
    # Hackathon spec: must respond to POST /reset
    try:
        data = await request.json()
        task_id = data.get("task_id", "task_1_basic_dispatch")
    except:
        task_id = "task_1_basic_dispatch"
        
    state = env.reset(task_id=task_id)
    return {"state": state}

@app.post("/step")
async def step(request: Request):
    # Hackathon spec: /step endpoint
    try:
        data = await request.json()
    except:
        data = {"action": "wait"}
        
    state, reward, done, info = env.step(data)
    return {"state": state, "reward": reward, "done": done, "info": info}

@app.get("/state")
def get_state():
    # Hackathon spec: /state endpoint
    return {"state": env.state}

if __name__ == "__main__":
    # Hugging Face Spaces strictly run on port 7860
    uvicorn.run(app, host="0.0.0.0", port=7860)
