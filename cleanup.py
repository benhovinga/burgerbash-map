import json
import re

INPUT_FILE = "listings.json"
OUTPUT_FILE = "listings_clean.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    listings = json.load(f)

for listing in listings:

    # 1. Swap lat/long if longitude is not negative
    lat = listing.get("latitude")
    lon = listing.get("longitude")
    if lat is not None and lon is not None:
        try:
            if float(lon) > 0:
                listing["latitude"], listing["longitude"] = lon, lat
        except ValueError:
            pass

    # 2. Rename "title" to "restaurant"
    if "title" in listing:
        listing["restaurant"] = listing.pop("title")

    # 3. Split "burgername" into name and price on the "*" character
    burgername = listing.get("burgername", "") or ""
    if "*" in burgername:
        name, raw_price = burgername.split("*", 1)
        listing["burgername"] = name.strip()
        listing["price"] = raw_price.strip()
    else:
        listing["price"] = None

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(listings, f, indent=2, ensure_ascii=False)

print(f"Cleaned {len(listings)} listing(s) → saved to {OUTPUT_FILE}")
