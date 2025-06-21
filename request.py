import requests
import json
from typing import Optional

# The base URL of your FastAPI service
BASE_URL = "http://127.0.0.1:8000"

def search_properties_with_requests(roi: Optional[float] = None, area: Optional[str] = None, cost: Optional[float] = None):
    """
    Calls the FastAPI /properties/search endpoint using the requests library.
    """
    endpoint = f"{BASE_URL}/properties/search"
    params = {}

    if roi is not None:
        params["roi"] = roi
    if area is not None:
        params["area"] = area
    if cost is not None:
        params["cost"] = cost

    print(f"Making GET request to: {endpoint} with params: {params}")
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status() # Raises an HTTPError for bad responses (4xx or 5xx)

        properties = response.json()
        print("Successfully retrieved properties:")
        print(json.dumps(properties, indent=2, ensure_ascii=False)) # Pretty print JSON
        return properties

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to the FastAPI service. Is it running? {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: The request timed out. {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return None

# --- Example Calls ---

print("\n--- Example 1: Search with ROI, Area, and Cost ---")
search_properties_with_requests(roi=0.065, area="Business Bay", cost=1500000.0)

print("\n--- Example 2: Search with only ROI and Cost (Area ignored) ---")
search_properties_with_requests(roi=0.07, cost=2000000.0)

print("\n--- Example 3: Search with only Area (ROI and Cost ignored) ---")
search_properties_with_requests(area="Arabian Ranches")

print("\n--- Example 4: Search with no parameters (should return all properties) ---")
search_properties_with_requests()

print("\n--- Example 5: Search with a non-existent area ---")
search_properties_with_requests(area="NonExistentArea")
