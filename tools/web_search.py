import os
from tavily import TavilyClient
from smolagents import tool
from dotenv import load_dotenv
load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_TOKEN")

@tool
def web_search(query: str) -> str:
    """
    Searches the internet to find current information, websites, and specific URLs.
    
    Use this tool when you need to find the official website of a company, discover 
    where a pricing page is located, or gather general search engine results. 
    
    CRITICAL: This tool only returns brief search snippets and URLs. It does NOT 
    read the full webpage. Once this tool provides you with a relevant URL, you 
    must use your text scraping tool to read the actual detailed content of that page.
    
    Args:
        query: The specific search term or question to look up
    """
    try:
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        response = tavily.search(query=query)
        formatted_response = "" 
        for result in response["results"][:5]:
            formatted_response += f"Title: {result['title']}, URL: {result['url']}, Content: {result['content']}\n"
        return formatted_response
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(web_search("Latest News on AI"))