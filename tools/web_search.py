import requests
from bs4 import BeautifulSoup
from smolagents import tool

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
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(f"https://www.google.com/search?q={query}", headers=headers, timeout=10, )
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            script.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print(web_search("Latest News on AI"))