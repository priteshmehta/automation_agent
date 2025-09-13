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

    async def get_text(self, locator):
        try:
            print(f"[TOOL] Getting text from: {locator}")
            el = await self.page.wait_for_selector(locator, timeout=5000)
            text = await el.inner_text()
            return {"status": "success", "text": text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_attribute(self, locator, attribute):
        try:
            print(f"[TOOL] Getting attribute '{attribute}' from: {locator}")
            el = await self.page.wait_for_selector(locator, timeout=5000)
            value = await el.get_attribute(attribute)
            return {"status": "success", "attribute": attribute, "value": value}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def check_visible(self, locator):
        try:
            print(f"[TOOL] Checking visibility for: {locator}")
            el = await self.page.wait_for_selector(locator, timeout=5000)
            visible = await el.is_visible()
            return {"status": "success", "visible": visible}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def check_enabled(self, locator):
        try:
            print(f"[TOOL] Checking enabled for: {locator}")
            el = await self.page.wait_for_selector(locator, timeout=5000)
            enabled = await el.is_enabled()
            return {"status": "success", "enabled": enabled}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def reload(self):
        try:
            print(f"[TOOL] Reloading page")
            await self.page.reload()
            await self.page.wait_for_timeout(1000)
            return {"status": "success"}
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
    },
    {
        "type": "function",
        "function": {
            "name": "get_text",
            "description": "Get inner text of an element",
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
            "name": "get_attribute",
            "description": "Get attribute value of an element",
            "parameters": {
                "type": "object",
                "properties": {
                    "locator": {"type": "string", "description": "CSS or XPath selector for the element"},
                    "attribute": {"type": "string", "description": "Attribute name to retrieve"}
                },
                "required": ["locator", "attribute"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_visible",
            "description": "Check if an element is visible",
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
            "name": "check_enabled",
            "description": "Check if an element is enabled",
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
            "name": "reload",
            "description": "Reload the current page",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]
