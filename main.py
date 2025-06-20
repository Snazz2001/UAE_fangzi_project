from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd # Import pandas

# Initialize the FastAPI application
app = FastAPI(
    title="Property Search Service",
    description="A service to search for properties based on ROI, Area, and Cost.",
    version="1.0.0"
)

# --- Data Models ---

class Property(BaseModel):
    """
    Represents a property with its details.
    """
    id: int = Field(..., description="Unique identifier for the property.")
    name: str = Field(..., description="Name or title of the property.")
    area: str = Field(..., description="The geographical area where the property is located (e.g., 'Business Bay').")
    cost: float = Field(..., gt=0, description="The total cost of the property in currency units (e.g., millions).")
    expected_roi: float = Field(..., ge=0, description="The expected Return on Investment for the property (as a percentage, e.g., 0.05 for 5%).")
    description: Optional[str] = Field(None, description="A brief description of the property.")
    address: Optional[str] = Field(None, description="The full address of the property.")

# --- Data Loading (Using Pandas DataFrame) ---
# Create a dictionary of data that mimics your DUMMY_PROPERTIES
# In a real scenario, you'd load this from a CSV, Excel, database, etc.
property_data = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8],
    "name": [
        "Luxury Apartment - Business Bay",
        "Penthouse Suite - Downtown Dubai",
        "Modern Villa - Arabian Ranches",
        "Studio Flat - Business Bay",
        "Commercial Office - JLT",
        "Premium Apartment - Business Bay",
        "Luxury Condo - Palm Jumeirah",
        "Townhouse - Business Bay",
    ],
    "area": [
        "Business Bay",
        "Downtown Dubai",
        "Arabian Ranches",
        "Business Bay",
        "JLT",
        "Business Bay",
        "Palm Jumeirah",
        "Business Bay",
    ],
    "cost": [
        1_500_000.00,
        5_000_000.00,
        3_000_000.00,
        800_000.00,
        2_000_000.00,
        1_200_000.00,
        7_000_000.00,
        2_800_000.00,
    ],
    "expected_roi": [0.07, 0.04, 0.06, 0.08, 0.075, 0.065, 0.05, 0.055],
    "description": [
        "Spacious 2-bedroom apartment with canal views.",
        "Exclusive penthouse with panoramic city views.",
        "Family villa with private garden and pool access.",
        "Compact studio ideal for young professionals.",
        "Grade A office space near metro station.",
        "1-bedroom apartment with high rental yield potential.",
        "Waterfront condo with private beach access.",
        "Spacious townhouse in a prime Business Bay location.",
    ],
    "address": [
        "Tower A, Business Bay",
        "Burj Views, Downtown Dubai",
        "Al Reem 1, Arabian Ranches",
        "The Executive Towers, Business Bay",
        "Cluster D, Jumeirah Lakes Towers",
        "Bay Square, Business Bay",
        "Shoreline Apartments, Palm Jumeirah",
        "Marasi Drive, Business Bay",
    ],
}

# Create the DataFrame
df_properties = pd.DataFrame(property_data)

# Convert DataFrame rows to a list of Property Pydantic models
# This is done once when the application starts
ALL_PROPERTIES: List[Property] = [Property(**row) for row in df_properties.to_dict(orient="records")]


# --- Endpoint Definition ---

@app.get("/properties/search", response_model=List[Property])
async def search_properties(
    roi: float = Query(..., ge=0.0, description="Minimum desired Return on Investment (as a float, e.g., 0.05 for 5%)."),
    area: str = Query(..., description="Desired property area (e.g., 'Business Bay', case-insensitive)."),
    cost: float = Query(..., gt=0.0, description="Maximum desired property cost (e.g., 1000000.0 for 1 Million).")
):
    """
    Searches for properties that meet the specified ROI, area, and cost criteria.

    - **roi**: The minimum expected Return on Investment you are looking for.
      (e.g., `0.07` for 7%).
    - **area**: The specific geographical area you are interested in.
      (e.g., `'Business Bay'`). The search is case-insensitive.
    - **cost**: The maximum budget for the property.
      (e.g., `1000000.0` for 1 Million AED/USD).

    Returns a list of properties that satisfy all conditions.
    """
    found_properties: List[Property] = []
    normalized_area = area.lower() # Normalize area for case-insensitive comparison

    # Filter the ALL_PROPERTIES list, which was created from the DataFrame
    for prop in ALL_PROPERTIES:
        # Check ROI condition
        roi_condition = prop.expected_roi >= roi

        # Check Area condition (case-insensitive)
        area_condition = prop.area.lower() == normalized_area

        # Check Cost condition
        cost_condition = prop.cost <= cost

        if roi_condition and area_condition and cost_condition:
            found_properties.append(prop)

    if not found_properties:
        # It's good practice to provide a clear message if no properties are found
        # instead of just an empty list, but an empty list is also valid.
        # For this example, we'll return an empty list if no properties match.
        pass

    return found_properties

# --- Example Usage (How to run and test) ---
# To run this service, save the code as a Python file (e.g., main.py).
# Then, open your terminal in the same directory and run:
# pip install "fastapi[all]" pandas # Install FastAPI, Uvicorn, and Pandas
# uvicorn main:app --reload

# Once running, you can access the interactive API documentation at:
# [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
# Or test the endpoint directly using a URL like:
# [http://127.0.0.1:8000/properties/search?roi=0.06&area=Business%20Bay&cost=1500000.0](http://127.0.0.1:8000/properties/search?roi=0.06&area=Business%20Bay&cost=1500000.0)
