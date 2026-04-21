import requests
from bs4 import BeautifulSoup

# ── Configuration ──────────────────────────────────────────────────────────────
URL = "https://burgerbash.ca/burger-lineup/"  # <-- change this to your target URL
# ───────────────────────────────────────────────────────────────────────────────


def fetch_links(url: str) -> list[dict]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    container = soup.find(id="listeo-listings-container")
    if container is None:
        print("Element with id='listeo-listings-container' was not found on the page.")
        return []

    links = []
    for tag in container.find_all("a", href=True):
        links.append(
            {
                "text": tag.get_text(strip=True) or "(no text)",
                "href": tag["href"],
            }
        )

    return links


if __name__ == "__main__":
    print(f"Fetching: {URL}\n")
    results = fetch_links(URL)

    if results:
        print(f"Found {len(results)} link(s):\n")
        for i, link in enumerate(results, start=1):
            print(f"  {i:>3}. {link['text']}")
            print(f"       {link['href']}\n")
    else:
        print("No links found.")
