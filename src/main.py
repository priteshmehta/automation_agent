import asyncio
from src.web_captain import WebCaptain

if __name__ == "__main__":
    captain = WebCaptain()
    captain.run(workflow_files=["../workflows/test_case_login_voice.yaml"])
