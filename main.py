import argparse
from rich.console import Console
from rich.markdown import Markdown
from agents.synthesizer import run_synthesizer_agent

def main():
    console = Console()
    parser = argparse.ArgumentParser(description="Autonomous Competitive Research Swarm")
    parser.add_argument("--topic", type=str, required=True, help="Topic you want to research. Separate multiple topics with commas.")
    parser.add_argument("--persona", type=str, required=True, help="The persona of the agent")
    args = parser.parse_args()

    topics = [t.strip() for t in args.topic.split(",")]
    final_result = Markdown(run_synthesizer_agent(topics, args.persona))
    console.print(final_result)

if __name__ == "__main__":
    main()