from agents.researcher import run_research_agent
from smolagents import CodeAgent, LiteLLMModel


llm = LiteLLMModel(model="ollama_chat/qwen3:8b")

def run_synthesizer_agent(topics: list[str], persona: str):
    with open("prompts/synthesizer.md", "r") as f:
        manager_prompt = f.read()

    results = []
    
    for topic in topics:
        result = run_research_agent(topic, persona)
        results.append(result)

    topics_string = ", ".join(topics)
    raw_data_context = "\n\n--- NEXT REPORT ---\n\n".join(results)
    
    task_prompt = f"""
    TARGETS ANALYZED: {topics_string}

    IMMEDIATE ACTIONS REQUIRED:
    1. Read your system prompt to understand your Executive Editor persona and the required Markdown table format.
    2. Read the following raw field reports gathered by your research agents.
    3. Cross-reference the data and output ONLY the final comparative Markdown table. Do not include introductory text.

    ========================================
    RAW FIELD REPORTS FOR SYNTHESIS:
    ========================================
    {raw_data_context}
    ========================================
    """

    agent = CodeAgent(
        model=llm,
        tools=[],
        system_prompt=manager_prompt
    )

    final_result = agent.run(task_prompt)
    return final_result