import argparse
from agents.researcher import run_research_agent

def main():
    results = []
    parser = argparse.ArgumentParser(description="Autonomous Competitive Research Swarm")
    parser.add_argument("--topic", type=str, required=True, help="Topic you want to research. Separate multiple topics with commas.")
    parser.add_argument("--persona", type=str, required=True, help="The persona of the agent")
    args = parser.parse_args()

    topics = [t.strip() for t in args.topic.split(",")]
    for topic in topics:
        result = run_research_agent(topic, args.persona)
        results.append(result)
    
    print(results)

if __name__ == "__main__":
    main()