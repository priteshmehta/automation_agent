import asyncio
import json
import base64
import config
from playwright.async_api import async_playwright
from openai import AsyncOpenAI
import os
import sys
import time
from tool_executor import TOOL_SCHEMAS, ToolExecutor
from workflow_loader import WorkflowLoader
from dotenv import load_dotenv      

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
if os.getenv("BASE_URL") != "":
    client = AsyncOpenAI(base_url=os.getenv("BASE_URL"), api_key=os.getenv("OPENAI_API_KEY"))
else:
    client = AsyncOpenAI()

async def extract_visible_dom(page):
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

async def get_gpt_locator(dom_elements, gpt_hint):
    system_prompt = (
        """
        You are a smart and reliable web automation agent.
        Your task is to help a browser automation script identify the correct HTML element to interact with, based on a user's goal and a list of visible DOM elements.

        Use the following information:
        - The user **goal** (what they are trying to do)
        - A list of **visible DOM elements** (including tag, text content, and a preview of the outer HTML)
        - Any **locator hint** provided in the goal

        Return a **unique and robust CSS or XPath locator string** that can be used with **Playwright** to find and interact with the element.

        Output only the best locator string with format "locator_type|locator_string", preferring **CSS selectors** when possible. The locator should be reliable across sessions and specific enough to uniquely identify the intended element.
    """
    )
    user_prompt = (
        f"Locator hint: {gpt_hint}\n"
        f"DOM Elements:\n{json.dumps(dom_elements, indent=2)}\n"
        "CSS is preferred if return xpath locator if CSS locator doesn't is not possible."
    )
    #print("\n[GPT TEXTUAL SUGGESTION PROMPT]\n", user_prompt)
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

async def capture_and_analyze_screenshot(page, goal_text):
    path = "page_screenshot.png"
    await page.screenshot(path=path, full_page=True)

    vision_prompt = (
        f"Here is a screenshot of a webpage. Act like human, Based on the user goal: '{goal_text}' check if it matches and return result as true or flast with one line reasoning with format true/flase|reasoning."
    )

    with open(path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful visual assistant that can analyze webpage screenshots."},
            {"role": "user", "content": [
                {"type": "text", "text": vision_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
            ]}
        ],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()


async def try_to_click_based_on_hint(page, locator):
    print("\n[TRYING TO CLICK BASED ON SELECTOR]\n")
    locator_type,locator_string = locator.split("|")
    try:
        if locator_type.lower() == "xpath":
            print(f"Clicking using XPath: {locator_string}")
            el = await page.wait_for_selector(f"xpath={locator_string}", timeout=5000)
        elif locator_type.lower() == "css":
            print(f"Clicking using CSS: {locator_string}")
            el = await page.wait_for_selector(locator_string, timeout=5000)
        else:
            print(f"Unknown locator type: {locator_type}")
            return False
        await el.click()    
        print("Click successful.")
        return True
    except Exception as e:
        print("Failed to click using locator:", e)
        return False

async def run_agentic_workflow(page, workflow_path):
     variables = {
        "username": config.USER_NAME,   # Use config.py values
        "password": config.USER_PASSWORD
    }
    loader = WorkflowLoader(workflow_path, variables=variables)
    workflow = loader.load_combined_workflow()
    await page.goto(workflow["url"])
    await page.wait_for_timeout(4000)

    executor = ToolExecutor(page)

    for phase in ["setup", "steps", "cleanup"]:
        for step in workflow.get(phase, []):
            time.sleep(5)
            goal = step["goal"] if isinstance(step, dict) else step
            print(f"\n[{phase.upper()} STEP] Goal: {goal}\n")
            dom = await extract_visible_dom(page)

            response = await client.chat.completions.create(
                model="gpt-4o",
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                messages=[
                    {"role": "system", "content": "You are a web automation agent. Given the goal and DOM context, choose the correct action using one of the available tools. element locator should be CSS or XPath so playwright can use it."},
                    {"role": "user", "content": f"Goal: {goal}\nDOM: {json.dumps(dom)}"}
                ]
            )
            print("AI response:", response.choices[0].message)
            tool_call = response.choices[0].message.tool_calls[0]
            tool_name = tool_call.function.name
            print(f"[TOOL CALL] Name: {tool_name}, Arguments: {tool_call.function.arguments}")
            arguments = json.loads(tool_call.function.arguments)

            if hasattr(executor, tool_name):
                result = await getattr(executor, tool_name)(**arguments)
                print(f"[RESULT] {result}")
            else:
                print(f"[ERROR] No handler for tool '{tool_name}'")


async def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    workflow_path = os.path.join(cwd, "workflows", "test_case_login_voice.yaml")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await run_agentic_workflow(page, workflow_path)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
