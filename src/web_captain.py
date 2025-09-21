import os
from playwright.async_api import async_playwright
import src.config
from src.llm_client import LlmClientFactory
from src.locator_selector import LocatorSelector
from src.logger import JsonLogger
from src.workflow_runner import WorkflowRunner
import asyncio

class WebCaptain:
    def __init__(self):
        self.logger = JsonLogger()
        self.client = LlmClientFactory.create(src.config)
        self.workflow_runner = WorkflowRunner(self.client, src.config, self.logger)

    async def _run_async(self, workflow_files=None):
        self.logger.log("Starting the web agent...")
        cwd = os.path.dirname(os.path.abspath(__file__))
        for workflow in workflow_files:
            workflow_path = os.path.join(cwd, workflow)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            await self.workflow_runner.run_agentic_workflow(page, workflow_path)
            await browser.close()

    def run(self, workflow_files=None):
        asyncio.run(self._run_async(workflow_files=workflow_files))

