🚑 PulsePath

> Autonomous emergency ambulance dispatch using Reinforcement Learning.

Built for the **OpenEnv × Scaler Hackathon**.

---

## What it does

PulsePath simulates an RL environment where an ambulance agent navigates a 5×5 grid to respond to emergencies as fast as possible. The agent is scored on how efficiently it dispatches — prioritizing high-severity cases and minimizing response time.

---

## Environment

| Property | Value |
|---|---|
| Grid size | 5×5 |
| Max steps per episode | 15 |
| Action space | `up`, `down`, `left`, `right`, `wait` |
| Observation | Ambulance position + emergency positions + priorities |

### Tasks

| Task | Description |
|---|---|
| `task_1_basic_dispatch` | Single high-priority emergency at [4,4] |
| `task_2_triage_dilemma` | Two emergencies with conflicting priorities |
| `task_3_fleet_management` | Dynamic dispatch with mid-grid emergency |

### Scoring

Each task returns a score strictly in **(0, 1)**:
- `0.99` → all emergencies resolved
- Partial scores based on completion progress + Manhattan distance to nearest emergency

---

## Setup

```bash
pip install -r requirements.txt
```

### Run locally

```bash
python inference.py
```

### Run with Docker

```bash
docker build -t pulsepath .
docker run -e HF_TOKEN=your_token pulsepath
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `API_BASE_URL` | LLM API endpoint | `https://api.openai.com/v1` |
| `MODEL_NAME` | Model to use for fallback LLM | `gpt-3.5-turbo` |
| `HF_TOKEN` | API key / HuggingFace token | None |

---

## Project Structure
├── ambulance_env.py   # RL environment (grid, rewards, task definitions)
├── inference.py       # Agent loop + LLM fallback + score output
├── Dockerfile         # Container setup for submission
├── openenv.yaml       # Hackathon config
└── requirements.txt

---

## How the agent works

1. At each step, the agent first tries to call a local RL model server at `http://127.0.0.1:7860/act`
2. If that's unavailable, it falls back to prompting an LLM with the current grid state
3. The LLM returns a JSON action `{"action": "up"}` which the environment executes
4. Episode ends when all emergencies are resolved or max steps are reached

---

## Reward Structure

| Event | Reward |
|---|---|
| Reaching a high-priority emergency | +0.99 |
| Reaching a low-priority emergency | +0.5 |
| Invalid action | -0.1 |
| Each step taken | -0.05 |

All rewards and scores are clamped to **(0.001, 0.999)** to satisfy platform validation.
