import json
import requests
from bs4 import BeautifulSoup

# ── Configuration ──────────────────────────────────────────────────────────────
URL = "https://burgerbash.ca/burger-lineup/"  # <-- change to your target URL
OUTPUT_FILE = "listings.json"  # <-- output file name
# ───────────────────────────────────────────────────────────────────────────────


def fetch_listings(url: str) -> list[dict]:
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

    listings = []
    for tag in container.find_all("a", href=True):
        # Collect all data-* attributes, stripping the "data-" prefix
        data_attrs = {
            key[5:]: value
            for key, value in tag.attrs.items()
            if key.startswith("data-")
        }

        listings.append(
            {
                "href": tag["href"],
                "text": tag.get_text(strip=True) or None,
                **data_attrs,
            }
        )

    return listings


if __name__ == "__main__":
    print(f"Fetching: {URL}\n")
    results = fetch_listings(URL)

    if results:
        print(f"Found {len(results)} listing(s).")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Saved to {OUTPUT_FILE}")
    else:
        print("No listings found.")
