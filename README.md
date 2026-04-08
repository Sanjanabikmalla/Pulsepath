

PulsePath is a custom reinforcement learning environment we built for the Meta x PyTorch x Scaler Hackathon. 

Instead of doing a generic grid game, we wanted to simulate a real logistics problem: ambulance dispatch. Dispatchers have to constantly balance distance (who is closest) with triage rules (who is most critical). PulsePath forces an AI agent to learn how to make these routing decisions on the fly without letting critical cases expire.

## The 3 OpenEnv Tasks

We structured our `AmbulanceDispatchEnv` to ramp up in difficulty to fully test the logic of the LLM:

1. **Basic Dispatch**: A simple pathfinding test. One ambulance, one critical emergency on a 5x5 grid. The grader strictly penalizes wasted movement and bumping into grid boundaries.
2. **The Triage Dilemma**: The agent is presented with a low-severity case (close by) and a high-severity case (far away). The grader instantly fails the agent (score: 0.0) if it doesn't prioritize the critical patient first.
3. **Fleet Management**: Continuous spawning of mixed-severity emergencies. The AI has to manage a fleet without duplicating assignments or letting the priority queue collapse.

## Hackathon Compliance

A big focus for us was making sure the evaluator script wouldn't crash when running our environment. 
- All 3 graders return tightly clamped `[0.0, 1.0]` float scores.
- `inference.py` pulls from `API_BASE_URL` dynamically and catches fallback exceptions if the LLM hallucinated bad JSON.
- Strict `[START]`, `[STEP]`, and `[END]` stdout logging format is maintained exactly to spec.

## Tech Stack
- Vanilla Python 3.11
- OpenEnv
- OpenAI SDK

Built for the 2026 Hackathon rollout.
