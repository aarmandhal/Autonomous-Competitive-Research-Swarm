import requests
from bs4 import BeautifulSoup
from smolagents import decorator

@decorator.tool
def scrape_text(url: str) -> str:
    """Scrape Text From Any Given URL."""
    try:
        response = requests.get(url, timeout=10)
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