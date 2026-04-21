import json
import time
import requests
from bs4 import BeautifulSoup

# ── Configuration ──────────────────────────────────────────────────────────────
URL = "https://burgerbash.ca/burger-lineup/"  # <-- change to your target URL
OUTPUT_FILE = "listings.json"  # <-- output file name
# ───────────────────────────────────────────────────────────────────────────────

EXCLUDE_ATTRS = {"listing-type", "classifieds-price", "icon"}

GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
GEOCODE_HEADERS = {"User-Agent": "burger-scraper/1.0"}


def geocode(address: str) -> tuple[str, str] | tuple[None, None]:
    """Look up lat/long for an address using the free Nominatim API."""
    if not address or not address.strip():
        return None, None
    try:
        resp = requests.get(
            GEOCODE_URL,
            params={"q": address, "format": "json", "limit": 1},
            headers=GEOCODE_HEADERS,
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            return results[0]["lat"], results[0]["lon"]
    except Exception as e:
        print(f"  ⚠️  Geocoding failed for '{address}': {e}")
    return None, None


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
        # Collect all data-* attributes, stripping the "data-" prefix and skipping excluded keys
        data_attrs = {
            key[5:]: value
            for key, value in tag.attrs.items()
            if key.startswith("data-") and key[5:] not in EXCLUDE_ATTRS
        }

        burgername_tag = tag.find(class_="burgername")
        burgername = burgername_tag.get_text(strip=True) if burgername_tag else None

        # Fill in missing lat/long via geocoding
        lat = data_attrs.get("latitude")
        lon = data_attrs.get("longitude")

        if not lat or not lon:
            address = data_attrs.get("friendly-address") or data_attrs.get(
                "address", ""
            )
            title = data_attrs.get("title", "")
            print(f"  📍 Geocoding '{title}' using: {address!r}")
            lat, lon = geocode(address)
            data_attrs["latitude"] = lat
            data_attrs["longitude"] = lon
            # Nominatim rate limit: max 1 request/second
            time.sleep(1)

        listings.append(
            {
                "href": tag["href"],
                "burgername": burgername,
                **data_attrs,
            }
        )

    return listings


if __name__ == "__main__":
    print(f"Fetching: {URL}\n")
    results = fetch_listings(URL)

    if results:
        print(f"\nFound {len(results)} listing(s).")

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Saved to {OUTPUT_FILE}")
    else:
        print("No listings found.")
