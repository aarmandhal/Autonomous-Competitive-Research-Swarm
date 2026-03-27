import requests
from bs4 import BeautifulSoup
from smolagents import tool

@tool
def scrape_text(url: str) -> str:
    """
    Fetches and extracts clean, human-readable text from any specific webpage.
    
    Use this tool ONLY when you already have a direct, valid HTTP or HTTPS URL 
    and you need to read the actual contents of that specific page (e.g., to read 
    a competitor's pricing page, feature list, or documentation). 
    
    Do NOT use this tool to search the web (e.g., do not pass "Google search 
    competitor pricing" into this tool). It only accepts raw URLs.
    
    Args:
        url: The full, valid HTTP/HTTPS URL of the target website.
        
    Returns:
        A single string containing the cleaned text of the webpage, stripped of all 
        HTML tags, scripts, navigation menus, and footers. If the scrape fails, 
        it will return an error message string explaining why.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
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
        return f"Error scraping {url}: {e}"

if __name__ == "__main__":
    print(scrape_text("https://www.google.com"))
