#!/usr/bin/env python3
"""
Alepa city bikes (Käpylä): print live availability for
- Pohjolankatu (smoove:145)
- Koskelantie  (smoove:142)

Uses Digitransit Routing API v2 (GraphQL).
Reads API key from environment:
  DIGITRANSIT_KEY  (preferred)
or DIGITRANSIT_API_KEY (fallback, for older .env)
"""

import os
import requests

# Optional local .env support (does nothing if package not installed)
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

API_KEY = (os.getenv("DIGITRANSIT_KEY") or os.getenv("DIGITRANSIT_API_KEY") or "").strip()
GRAPHQL_URL = "https://api.digitransit.fi/routing/v2/hsl/gtfs/v1"

QUERY = """
{
  pohjolankatu: vehicleRentalStation(id: "smoove:145") {
    name
    availableVehicles { byType { count vehicleType { formFactor } } }
    availableSpaces   { byType { count vehicleType { formFactor } } }
  }
  koskelantie: vehicleRentalStation(id: "smoove:142") {
    name
    availableVehicles { byType { count vehicleType { formFactor } } }
    availableSpaces   { byType { count vehicleType { formFactor } } }
  }
}
"""

def sum_bicycles(section: dict) -> int:
    total = 0
    for item in (section or {}).get("byType", []):
        vt = (item.get("vehicleType") or {}).get("formFactor")
        if vt == "BICYCLE":
            total += int(item.get("count") or 0)
    return total

def main() -> None:
    if not API_KEY:
        raise SystemExit("Missing DIGITRANSIT_KEY. Put it in your .env or environment.")

    headers = {"Content-Type": "application/json", "digitransit-subscription-key": API_KEY}
    r = requests.post(GRAPHQL_URL, headers=headers, json={"query": QUERY}, timeout=20)

    print("HTTP", r.status_code, r.headers.get("Content-Type"))
    if r.status_code != 200:
        # Show first part of the body to explain the error (endpoint, key, etc.)
        print(r.text[:400])
        r.raise_for_status()

    payload = r.json()
    if "errors" in payload:
        raise SystemExit(f"GraphQL errors: {payload['errors']}")

    data = payload.get("data", {})
    for alias in ("pohjolankatu", "koskelantie"):
        node = data.get(alias)
        if not node:
            print(f"{alias}: not found in response")
            continue
        bikes = sum_bicycles(node.get("availableVehicles", {}))
        spaces = sum_bicycles(node.get("availableSpaces", {}))
        print(f"{node['name']}: {bikes} bikes available, {spaces} spaces free")

if __name__ == "__main__":
    main()
