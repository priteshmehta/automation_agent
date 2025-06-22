
class ToolExecutor:
    def __init__(self, page):
        self.page = page

    async def click(self, locator):
        try:
            print(f"[TOOL] Clicking: {locator}")
            el = await self.page.wait_for_selector(locator, timeout=5000)
            await el.evaluate("el => el.style.outline = '3px solid red'")
            await self.page.wait_for_timeout(1500)
            await el.click()
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def type(self, locator, text):
        try:
            print(f"[TOOL] Typing into: {locator} text='{text}'")
            el = await self.page.wait_for_selector(locator, timeout=5000)
            await el.click()
            await el.type(text)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def wait_for(self, locator):
        try:
            print(f"[TOOL] Waiting for: {locator}")
            await self.page.wait_for_selector(locator, timeout=5000)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    async def navigate_to(self, url):
        try:
            print(f"[TOOL] Navigating to: {url}")
            await self.page.goto(url)
            await self.page.wait_for_timeout(2000)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def take_screenshot(self, filename):
        try:
            print(f"[TOOL] Taking screenshot: {filename}")
            await self.page.screenshot(path=filename, full_page=True)
            return {"status": "success", "file": filename}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Tool function schemas for OpenAI Function Calling
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "click",
            "description": "Click on an element by locator",
            "parameters": {
                "type": "object",
                "properties": {
                    "locator": {"type": "string", "description": "CSS or XPath selector for the element"}
                },
                "required": ["locator"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "type",
            "description": "Type text into an input field",
            "parameters": {
                "type": "object",
                "properties": {
                    "locator": {"type": "string"},
                    "text": {"type": "string"}
                },
                "required": ["locator", "text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "wait_for",
            "description": "Wait for an element to appear",
            "parameters": {
                "type": "object",
                "properties": {
                    "locator": {"type": "string"}
                },
                "required": ["locator"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "navigate_to",
            "description": "Navigate to a given URL",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Target URL to navigate to"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Capture and save a screenshot of the current page",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Filename to save the screenshot as"}
                },
                "required": ["filename"]
            }
        }
    }
]
