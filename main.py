import asyncio
import config
from llm_client import LlmClientFactory
from playwright.async_api import async_playwright
import os
from locator_selector import LocatorSelector
from logger import JsonLogger
from workflow_runner import WorkflowRunner

client = LlmClientFactory.create(config)
logger = JsonLogger() 
workflow_runner = WorkflowRunner(client)

async def main():
    logger.log("Starting the web agent...")
    cwd = os.path.dirname(os.path.abspath(__file__))
    workflow_path = os.path.join(cwd, "workflows", "test_case_login_voice.yaml")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await workflow_runner.run_agentic_workflow(page, workflow_path)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
