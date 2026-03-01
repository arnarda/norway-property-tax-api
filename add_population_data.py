#!/usr/bin/env python3
"""
Fetch population data and municipality codes from SSB table 11342
and merge into norwegian-municipalities-complete-ssb-2025.json
"""

import json
import urllib.request
import sys
from datetime import datetime

JSON_FILE = "norwegian-municipalities-complete-ssb-2025.json"
SSB_TABLE_URL = "https://data.ssb.no/api/v0/no/table/11342"
TARGET_YEAR = "2025"

# Official Norwegian municipality codes (2025) mapped to names for validation
# SSB Region codes use 4-digit format: FFKK where FF=fylke, KK=kommune


def fetch_ssb_metadata():
    """Get available region codes from SSB."""
    req = urllib.request.Request(SSB_TABLE_URL)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_municipality_codes(meta):
    """Extract 4-digit municipality codes from SSB metadata, excluding non-municipality entries."""
    exclude_prefixes = ("23", "25", "99")
    codes = []
    code_to_name = {}
    for var in meta["variables"]:
        if var["code"] == "Region":
            for v, t in zip(var["values"], var["valueTexts"]):
                if len(v) == 4 and not v.startswith(exclude_prefixes):
                    codes.append(v)
                    clean_name = t.split(" (")[0].strip()
                    code_to_name[v] = clean_name
    return codes, code_to_name


def fetch_population_data(municipality_codes):
    """Query SSB for population data."""
    query = {
        "query": [
            {
                "code": "Region",
                "selection": {"filter": "item", "values": municipality_codes},
            },
            {
                "code": "ContentsCode",
                "selection": {"filter": "item", "values": ["Folkemengde"]},
            },
            {
                "code": "Tid",
                "selection": {"filter": "item", "values": [TARGET_YEAR]},
            },
        ],
        "response": {"format": "json-stat2"},
    }

    data = json.dumps(query).encode("utf-8")
    req = urllib.request.Request(
        SSB_TABLE_URL, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def parse_population_response(response, code_to_name):
    """Parse json-stat2 response into {code: population} dict.
    
    When multiple codes map to the same name (historical vs current),
    prefer the entry with non-zero population (= current municipality).
    """
    dimensions = response["dimension"]
    region_dim = dimensions["Region"]
    region_ids = list(region_dim["category"]["index"].keys())

    values = response["value"]

    pop_by_code = {}
    pop_by_name = {}
    for i, code in enumerate(region_ids):
        population = values[i] if i < len(values) else None
        if population is not None:
            pop_by_code[code] = int(population)
            label = code_to_name.get(code, region_dim["category"]["label"].get(code, ""))
            # Remove year qualifiers like " (2020-2023)" or " (-2019)"
            base_label = label.split(" (")[0].strip()
            # SSB uses "SamiName - NorwegianName" format for bilingual municipalities
            parts = [p.strip() for p in base_label.split(" - ")]

            entry = {
                "code": code,
                "population": int(population),
                "name": parts[-1] if len(parts) > 1 else parts[0],
            }

            for part in parts:
                norm_name = part.lower()
                existing = pop_by_name.get(norm_name)
                if existing is None or (int(population) > 0 and existing["population"] == 0):
                    pop_by_name[norm_name] = entry
    return pop_by_code, pop_by_name


def normalize(name):
    """Normalize municipality name for matching."""
    return (
        name.lower()
        .replace(" - ", "-")
        .replace("–", "-")
        .strip()
    )


def match_municipality(muni_name, pop_by_name, code_to_name):
    """Try to match a municipality name from our JSON to SSB data."""
    norm = normalize(muni_name)

    # Direct match
    if norm in pop_by_name:
        return pop_by_name[norm]

    # Try without parenthetical
    base = norm.split("(")[0].strip()
    if base in pop_by_name:
        return pop_by_name[base]

    # Try partial matching (SSB names sometimes have extra qualifiers)
    for ssb_name, data in pop_by_name.items():
        if norm in ssb_name or ssb_name in norm:
            return data

    # Try matching with common name variations
    variations = {
        "bo": "bø",
        "boe": "bø",
        "vaagan": "vågan",
        "vaaler": "våler",
        "raade": "råde",
        "rade": "råde",
        "aal": "ål",
        "karasjok": "kárásjohka",
        "kautokeino": "guovdageaidnu",
        "tana": "deatnu",
    }
    if norm in variations and variations[norm] in pop_by_name:
        return pop_by_name[variations[norm]]

    return None


def main():
    print(f"Loading {JSON_FILE}...")
    with open(JSON_FILE) as f:
        data = json.load(f)

    municipalities = data["municipalities"]
    print(f"Found {len(municipalities)} municipalities in JSON")

    print("\nFetching SSB metadata...")
    meta = fetch_ssb_metadata()
    codes, code_to_name = get_municipality_codes(meta)
    print(f"Found {len(codes)} municipality codes in SSB")

    print(f"\nFetching population data for {TARGET_YEAR}...")
    response = fetch_population_data(codes)
    pop_by_code, pop_by_name = parse_population_response(response, code_to_name)
    print(f"Got population data for {len(pop_by_code)} municipalities")

    matched = 0
    unmatched = []

    for muni in municipalities:
        result = match_municipality(muni["name"], pop_by_name, code_to_name)
        if result:
            muni["code"] = result["code"]
            muni["befolkning"] = result["population"]
            matched += 1
        else:
            unmatched.append(muni["name"])

    print(f"\nMatched: {matched}/{len(municipalities)}")
    if unmatched:
        print(f"Unmatched ({len(unmatched)}):")
        for name in sorted(unmatched):
            print(f"  - {name}")

    data["lastUpdated"] = datetime.now().strftime("%Y-%m-%d")
    data["population_source"] = f"SSB table 11342, year {TARGET_YEAR}"

    print(f"\nWriting updated {JSON_FILE}...")
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Done!")

    # Summary
    total_pop = sum(m.get("befolkning", 0) for m in municipalities)
    print(f"\nTotal population across matched municipalities: {total_pop:,}")

    return 0 if not unmatched else 1


if __name__ == "__main__":
    sys.exit(main())
