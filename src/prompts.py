def get_gpt_locator_system_prompt() -> str:
    return (
        "You are a smart and reliable web automation agent.\n"
        "Your task is to help a browser automation script identify the correct HTML element to interact with, based on a user's goal and a list of visible DOM elements.\n\n"
        "Use the following information:\n"
        "- The user **goal** (what they are trying to do)\n"
        "- A list of **visible DOM elements** (including tag, text content, and a preview of the outer HTML)\n"
        "- Any **locator hint** provided in the goal\n\n"
        "Return a **unique and robust CSS or XPath locator string** that can be used with **Playwright** to find and interact with the element.\n\n"
        "Output only the best locator string with format \"locator_type|locator_string\", preferring **CSS selectors** when possible. The locator should be reliable across sessions and specific enough to uniquely identify the intended element."
    )

def get_vision_system_prompt(goal_text: str) -> str:
    return (
        "Here is a screenshot of a webpage. Act like human, "
        f"Based on the user goal: '{goal_text}' check if it matches and return result "
        "as true or false with one line reasoning with format true/false|reasoning."
    )
# Add more