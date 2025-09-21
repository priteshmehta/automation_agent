import glob
import os
import argparse
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

    def _resolve_workflow_files(self, workflow_files):
        resolved_files = []
        cwd = os.path.dirname(os.path.abspath(__file__))

        if not workflow_files:
            return resolved_files

        for wf in workflow_files:
            wf_path = os.path.join(cwd, wf)
            if os.path.isdir(wf_path):
                # Add all .yaml/.yml files in the folder
                resolved_files.extend(
                    glob.glob(os.path.join(wf_path, "*.yaml")) +
                    glob.glob(os.path.join(wf_path, "*.yml"))
                )
            elif os.path.isfile(wf_path):
                resolved_files.append(wf_path)
            else:
                if os.path.isdir(wf):
                    resolved_files.extend(
                        glob.glob(os.path.join(wf, "*.yaml")) +
                        glob.glob(os.path.join(wf, "*.yml"))
                    )
                elif os.path.isfile(wf):
                    resolved_files.append(wf)
        return resolved_files
    
    async def _run_async(self, workflow_files=None):
        self.logger.log("Starting the web agent...")
        resolved_files = self._resolve_workflow_files(workflow_files)
        if not resolved_files:
            self.logger.log("No workflow files found.")
            return
        self.logger.log(f"Running Workflows: {resolved_files}")
        async with async_playwright() as p:
            for workflow_path in resolved_files:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context()
                page = await context.new_page()
                self.logger.log(f"Running workflow: {workflow_path}")
                await self.workflow_runner.run_agentic_workflow(page, workflow_path)
                await browser.close()

    def run(self, workflow_files=None):
        if workflow_files:
            asyncio.run(self._run_async(workflow_files=workflow_files))

def main():
    parser = argparse.ArgumentParser(description="Run WebCaptain automation agent.")
    parser.add_argument(
        "--workflows",
        nargs="+",
        required=True,
        help="List of workflow YAML files to execute."
    )
    args = parser.parse_args()
    captain = WebCaptain()
    print(f"CLI arguments: {args.workflows}")
    captain.run(workflow_files=args.workflows)

if __name__ == "__main__":
    main()
