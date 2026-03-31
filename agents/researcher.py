from tools.text_scraper import scrape_text
from tools.web_search import web_search
from smolagents import CodeAgent, LiteLLMModel

llm = LiteLLMModel(model="ollama_chat/qwen3:8b")
