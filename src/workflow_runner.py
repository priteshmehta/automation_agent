import time
import json
import config
from src.locator_selector import LocatorSelector
from src.tool_executor import TOOL_SCHEMAS, ToolExecutor
from src.workflow_loader import WorkflowLoader
from src.logger import JsonLogger

class WorkflowRunner:
    def __init__(self, client, logger = None):
        self.client = client
        self.config = config
        self.dom_locator = LocatorSelector(client, self.config)
        self.logger = logger if logger else JsonLogger()

    async def run_agentic_workflow(self, page, workflow_path):
        variables = {
            "username": self.config.USER_NAME,  
            "password": self.config.USER_PASSWORD
        }
        loader = WorkflowLoader(workflow_path, variables=variables)
        workflow = loader.load_combined_workflow()
        await page.goto(self.config.APP_URL)
        await page.wait_for_timeout(2000)

        executor = ToolExecutor(page, self.logger)

        for phase in ["setup", "steps", "cleanup"]:
            for step in workflow.get(phase, []):
                time.sleep(3)
                goal = step["goal"] if isinstance(step, dict) else step
                self.logger.log(f"[{phase.upper()} STEP] Goal: {goal}\n")
                dom = await self.dom_locator.extract_visible_dom(page)
                response = await self.client.chat(
                    model=self.config.LLM_MODEL,
                    tools=TOOL_SCHEMAS,
                    tool_choice="auto",
                    messages=[
                        {"role": "system", "content": "You are a web automation agent. Given the goal and DOM context, choose the correct action using one of the available tools. element locator should be CSS or XPath so playwright can use it."},
                        {"role": "user", "content": f"Goal: {goal}\nDOM: {json.dumps(dom)}"}
                    ]
                )
                #self.logger.log(f"LLM Response: {response.choices[0].message}")
                tool_calls = getattr(response.choices[0].message, "tool_calls", None)
                if not tool_calls:
                    self.logger.log(f"[ERROR] No tool calls returned for goal: {goal}")
                    continue

                tool_call = tool_calls[0]
                tool_name = tool_call.function.name
                self.logger.log(f"[TOOL CALL] Name: {tool_name}, Arguments: {tool_call.function.arguments}")
                arguments = json.loads(tool_call.function.arguments)

                if hasattr(executor, tool_name):
                    result = await getattr(executor, tool_name)(**arguments)
                    self.logger.log(f"{result} [RESULT]")
                else:
                    self.logger.log(f"[ERROR] No handler for tool '{tool_name}'")