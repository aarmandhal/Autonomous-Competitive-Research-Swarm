from tools.text_scraper import scrape_text
from tools.web_search import web_search
from smolagents import CodeAgent, LiteLLMModel

llm = LiteLLMModel(model="ollama_chat/qwen3:8b")
task_prompt = f"""
    TARGET TO RESEARCH: {topic}

    IMMEDIATE ACTIONS REQUIRED:
    1. Read your system prompt to understand your specific persona, objectives, and Required Output Format.
    2. Execute your strict Tool Pipeline (Search -> Scrape) to gather data on the target above.
    3. Return ONLY the final structured output exactly as defined in your system prompt. Do not include conversational filler like 'Here is the report'.
    """

def run_research_agent(topic: str, persona: str):
    prompt_path = f"prompts/{persona}.md"
    with open(prompt_path, "r") as f:
        prompt_template = f.read()

    agent = CodeAgent(
        model=llm,
        tools=[web_search, scrape_text],
        system_prompt=prompt_template
    )

    result = agent.run(task_prompt)
    return result