from tools.text_scraper import scrape_text
from tools.web_search import web_search
from smolagents import CodeAgent, LiteLLMModel
import os
from dotenv import load_dotenv
load_dotenv()

llm = LiteLLMModel(model_id="gemini/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))


def run_research_agent(topic: str, persona: str):
    task_prompt = f"""
    TARGET TO RESEARCH: {topic}

    IMMEDIATE ACTIONS REQUIRED:
    1. Read your system prompt to understand your specific persona, objectives, and Required Output Format.
    2. Execute your strict Tool Pipeline (Search -> Scrape) to gather data on the target above.
    3. Return ONLY the final structured output exactly as defined in your system prompt. Do not include conversational filler like 'Here is the report'.
    """

    prompt_path = f"prompts/{persona}.md"
    
    with open(prompt_path, "r") as f:
        prompt_template = f.read()

    agent = CodeAgent(
        model=llm,
        tools=[web_search, scrape_text],
        instructions=prompt_template
    )

    result = agent.run(task_prompt)
    return result