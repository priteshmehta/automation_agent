# mcp_agent.py
import json

class MCPAgent:
    def __init__(self, llm_client, executor):
        self.llm = llm_client
        self.executor = executor

    async def run(self, goal, dom_elements):
        history = []
        print("\n[AGENT START] Goal:", goal)

        for step_num in range(10):  # max 10 steps
            messages = [
                {"role": "system", "content": "You are a web automation agent. You will decide the next action based on the goal and visible DOM."},
                {"role": "user", "content": json.dumps({
                    "goal": goal,
                    "dom": dom_elements,
                    "history": history
                }, indent=2)}
            ]

            response = await self.llm.chat(messages)

            try:
                command = json.loads(response)
                print(f"[STEP {step_num+1}] Command: {command}")
                action = command.get("action")
                params = command.get("params", {})

                if hasattr(self.executor, action):
                    result = await getattr(self.executor, action)(**params)
                else:
                    result = {"status": "error", "message": f"Unknown action: {action}"}

                history.append({"step": step_num+1, "command": command, "result": result})

                if result.get("status") == "success" and goal.lower().startswith("click"):
                    print("[AGENT] Goal reached or action complete.")
                    break

            except Exception as e:
                print("[AGENT ERROR]", str(e))
                break

        return history
