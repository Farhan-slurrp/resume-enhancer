import re
import requests
from bs4 import BeautifulSoup

def extract_urls_from_text(text: str) -> list[str]:
    return re.findall(r"https?://\S+", text)

def fetch_url_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        return f"[Failed to fetch {url}: {e}]"

def fetch_all_url_contents(urls: list[str]) -> str:
    return "\n\n".join(
        f"--- Content from {url} ---\n{fetch_url_content(url)}"
        for url in urls
    )