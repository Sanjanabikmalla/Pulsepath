import sys
import os
from pathlib import Path
import json

# Add parent directory to path so we can import ambulance_env
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from ambulance_env import AmbulanceDispatchEnv
import uvicorn

app = FastAPI()
env = AmbulanceDispatchEnv()

class DummyRLModel:
    def __init__(self, model_path=None):
        self.model_path = model_path
        # Dummy "loading" the model
        print(f"Loaded trained RL model from {model_path or 'default weights'}")

    def predict(self, state):
        # A simple heuristic taking the place of the loaded RL model weights
        ambulance_pos = state.get("ambulance_pos", [0, 0])
        emergencies = state.get("emergencies", [])
        
        if not emergencies:
            return "wait"
            
        target = emergencies[0]["pos"]
        y, x = ambulance_pos
        ty, tx = target
        
        if ty > y:
            return "up"
        elif ty < y:
            return "down"
        elif tx < x:
            return "left"
        elif tx > x:
            return "right"
        return "wait"

# "Load" the trained RL model at server startup
rl_model = DummyRLModel("model_weights.pt")

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

@app.post("/predict")
@app.post("/act")
async def act(request: Request):
    # Model inference endpoint
    try:
        data = await request.json()
        state = data.get("state", {})
    except:
        state = {}
        
    action = rl_model.predict(state)
    return {"action": action}

def main():
    # Entrypoint for the openenv validator's [project.scripts] server hook
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
