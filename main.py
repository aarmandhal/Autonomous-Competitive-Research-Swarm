import argparse
from agents.researcher import run_research_agent

def main():
    parser = argparse.ArgumentParser(description="Autonomous Competitive Research Swarm")
    parser.add_argument("--topic", type=str, required=True, help="The company or subject to research")
    parser.add_argument("--persona", type=str, required=True, help="The persona of the agent")
    args = parser.parse_args()

    result = run_research_agent(args.topic, args.persona)
    print(result)

if __name__ == "__main__":
    main()