class AmbulanceDispatchEnv:
    def __init__(self, config=None):
        self.config = config or {}
        self.grid_size = 5
        self.max_steps = 15
        self.current_step = 0
        self.task_id = "task_1_basic_dispatch"
        self.state = {}
        
    def reset(self, task_id="task_1_basic_dispatch"):
        self.current_step = 0
        self.task_id = task_id
        
        # TASK 1: Basic dispatch (One emergency)
        if task_id == "task_1_basic_dispatch":
            self.state = {
                "ambulance_pos": [0, 0],
                "emergencies": [{"pos": [4, 4], "priority": "high"}],
                "status": "active"
            }
        # TASK 2: Triage Dilemma (Two emergencies)
        elif task_id == "task_2_triage_dilemma":
            self.state = {
                "ambulance_pos": [0, 0],
                "emergencies": [
                    {"pos": [3, 0], "priority": "low"}, 
                    {"pos": [0, 4], "priority": "high"}
                ],
                "status": "active"
            }
        # TASK 3: Fleet Management
        else:
            self.task_id = "task_3_fleet_management"
            self.state = {
                "ambulance_pos": [0, 0],
                "emergencies": [{"pos": [2, 2], "priority": "high"}],
                "status": "active"
            }
            
        return self.state

    def step(self, action_dict):
        self.current_step += 1
        reward = -0.05
        done = False
        
        if self.state["status"] == "active":
            # Just in case the API gives us raw strings instead of JSON
            if isinstance(action_dict, dict):
                action = action_dict.get("action", "wait")
            else:
                action = str(action_dict).strip().lower()
            
            y, x = self.state["ambulance_pos"]
            
            if action == "up" and y < self.grid_size - 1:
                y += 1
            elif action == "down" and y > 0:
                y -= 1
            elif action == "left" and x > 0:
                x -= 1
            elif action == "right" and x < self.grid_size - 1:
                x += 1
            elif action == "wait":
                pass
            else:
                reward -= 0.1 # Penalty for bad moves
                
            self.state["ambulance_pos"] = [y, x]
            
            # Check if ambulance landed on any emergency!
            remaining_emergencies = []
            for e in self.state["emergencies"]:
                if e["pos"] == self.state["ambulance_pos"]:
                    if e["priority"] == "high":
                        reward += 1.0 # Big reward!
                    else:
                        reward += 0.5
                else:
                    remaining_emergencies.append(e)
            
            self.state["emergencies"] = remaining_emergencies
            
            # If all emergencies are solved, episode over!
            if len(self.state["emergencies"]) == 0:
                self.state["status"] = "solved"
                done = True
                
        if self.current_step >= self.max_steps:
            done = True
            
        return self.state, reward, done, {}

    def evaluate_task(self):
        # OpenEnv Grader: Must return a strictly clamped float [0.0, 1.0]
        if self.state.get("status") == "solved":
            return 1.0
        return 0.0
