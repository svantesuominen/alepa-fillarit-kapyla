import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("DIGITRANSIT_API_KEY")

if not API_KEY:
    raise ValueError("No API key found. Please set DIGITRANSIT_API_KEY in your .env file.")

# GraphQL endpoint
url = "https://api.digitransit.fi/routing/v2/gtfs/hsl/index/graphql"

# Stations to query
stations = {
    "Pohjolankatu": "smoove:145",
    "Koskelantie": "smoove:142"
}

# GraphQL query template
query_template = """
{{
  vehicleRentalStation(id: "{station_id}") {{
    name
    availableVehicles {{
      byType {{
        count
        vehicleType {{
          formFactor
        }}
      }}
    }}
    availableSpaces {{
      byType {{
        count
        vehicleType {{
          formFactor
        }}
      }}
    }}
  }}
}}
"""

headers = {
    "Content-Type": "application/json",
    "digitransit-subscription-key": API_KEY
}

print("HTTP", end=" ")

# Fetch and print data for each station
for station_name, station_id in stations.items():
    query = query_template.format(station_id=station_id)
    response = requests.post(url, json={"query": query}, headers=headers)

    print(response.status_code, response.headers.get("Content-Type"))

    data = response.json()
    station_data = data["data"]["vehicleRentalStation"]
    available_bikes = station_data["availableVehicles"]["byType"][0]["count"]
    available_spaces = station_data["availableSpaces"]["byType"][0]["count"]
    print(f"{station_name}: {available_bikes} bikes available, {available_spaces} spaces free")
