import asyncio
import json
from agents.researcher import run_research_agent
from smolagents import CodeAgent, LiteLLMModel
from rich.console import Console
import os
from dotenv import load_dotenv
load_dotenv()

llm = LiteLLMModel(model_id="gemini/gemini-2.5-flash", api_key=os.getenv("GEMINI_API_KEY"))
console = Console()

async def fetch_research_task(topic: str, persona: str):
    return await asyncio.to_thread(run_research_agent, topic, persona)

async def run_synthesizer_agent(topics: list[str], persona: str):
    with open("prompts/synthesizer.md", "r") as f:
        manager_prompt = f.read()

    with console.status("[bold green]Booting up Swarm (Async Mode)...", spinner="dots") as status:
        
        status.update(f"[bold cyan]Dispatching {len(topics)} research agents concurrently...")
        
        tasks = [fetch_research_task(topic, persona) for topic in topics]
        
        results = await asyncio.gather(*tasks)

        stringified_results = []
        for r in results:
            if isinstance(r, dict):
                stringified_results.append(json.dumps(r, indent=2))
            else:
                stringified_results.append(str(r))

        topics_string = ", ".join(topics)
        raw_data_context = "\n\n--- NEXT REPORT ---\n\n".join(stringified_results)
        
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
            instructions=manager_prompt
        )

        status.update("[bold magenta]Field work complete. Synthesizing final matrix...")
        final_result = await asyncio.to_thread(agent.run, task_prompt)   
        
    return final_result