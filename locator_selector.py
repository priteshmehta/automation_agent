import json
from prompts import get_gpt_locator_system_prompt
import base64
import os
import config
import time
from prompts import get_gpt_locator_system_prompt, get_vision_system_prompt

class LocatorSelector:
    def __init__(self, client, config):
        self.client = client
        self.config = config

    async def extract_visible_dom(self, page):
        elements = await page.query_selector_all("button, a, input, span, div")
        visible_elements = []
        for el in elements:
            try:
                box = await el.bounding_box()
                if box:
                    tag = await el.evaluate("e => e.tagName.toLowerCase()")
                    text = (await el.inner_text()).strip()
                    selector = await page.evaluate("el => el.outerHTML", el)
                    visible_elements.append({
                        "tag": tag,
                        "text": text,
                        "selector_preview": selector[:120] + "..."
                    })
            except:
                continue
        return visible_elements

    async def capture_and_analyze_screenshot(self, page, goal_text):
        screenshot_dir = config.SCREENSHOT_DIR if hasattr(config, "SCREENSHOT_DIR") else "screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        path = os.path.join(screenshot_dir, f"page_screenshot_{int(time.time())}.png")
        await page.screenshot(path=path, full_page=True)

        vision_prompt = get_vision_system_prompt(goal_text)

        with open(path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")

        response = await self.client.chat(
            model=config.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful visual assistant that can analyze webpage screenshots."},
                {"role": "user", "content": [
                    {"type": "text", "text": vision_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
                ]}
            ],
            temperature=config.LLM_MODEL_TEMPERATURE
        )
        return response.choices[0].message.content.strip()

    async def select_locator(self, dom_elements, gpt_hint):
        user_prompt = (
            f"Locator hint: {gpt_hint}\n"
            f"DOM Elements:\n{json.dumps(dom_elements, indent=2)}\n"
            "CSS is preferred if return xpath locator if CSS locator doesn't is not possible."
        )
        response = await self.client.chat(
            model=self.config.LLM_MODEL,
            messages=[
                {"role": "system", "content": get_gpt_locator_system_prompt()},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.config.LLM_MODEL_TEMPERATURE
        )
        return response.choices[0].message.content.strip()