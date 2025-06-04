import requests
from bs4 import BeautifulSoup

def scrape_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find_all("a", class_="result__a")
    return [r.text for r in results[:5]]
