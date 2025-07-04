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
# Load the data from the CSV file
def load_properties_from_csv(file_path: str) -> pd.DataFrame:
    """
    Load properties from a CSV file into a Pandas DataFrame.
    """
    return pd.read_csv(file_path)

def convert_df_to_properties(df: pd.DataFrame) -> List[Property]:
    """
    Convert a Pandas DataFrame to a list of Property Pydantic models.
    """
    return [Property(**row) for row in df.to_dict(orient="records")]

csv_file_path = "/workspaces/anaconda/properties_2025_07_04.csv"

# Read the CSV file into a Pandas DataFrame
df_properties = load_properties_from_csv(csv_file_path)

# Convert DataFrame rows to a list of Property Pydantic models
# This is done once when the application starts
# ALL_PROPERTIES: List[Property] = [Property(**row) for row in df_properties.to_dict(orient="records")]
ALL_PROPERTIES: List[Property] = convert_df_to_properties(df_properties)


# --- Endpoint Definition ---
@app.get("/properties/search", response_model=List[Property])
async def search_properties(
    roi: Optional[float] = Query(None, ge=0.0, description="Minimum desired Return on Investment (as a float, e.g., 0.05 for 5%). If not provided, this criterion is ignored."),
    area: Optional[str] = Query(None, description="Desired property area (e.g., 'Business Bay', case-insensitive). If not provided, this criterion is ignored."),
    cost: Optional[float] = Query(None, gt=0.0, description="Maximum desired property cost (e.g., 1000000.0 for 1 Million). If not provided, this criterion is ignored.")
):
    """
    Searches for properties that meet the specified ROI, area, and cost criteria.
    Parameters are optional, and criteria will be ignored if not provided.
    """
    # Convert ALL_PROPERTIES to a DataFrame (assuming it's a list of dictionaries or objects)
    properties_df = pd.DataFrame([prop.dict() for prop in ALL_PROPERTIES])

    # Apply filters
    if roi is not None:
        properties_df = properties_df[properties_df['expected_roi'] >= roi]
    if area is not None:
        properties_df = properties_df[properties_df['area'].str.lower() == area.lower()]
    if cost is not None:
        properties_df = properties_df[properties_df['cost'] <= cost]

    # Convert filtered DataFrame back to list of Property objects
    found_properties = [Property(**row) for _, row in properties_df.iterrows()]

    return found_properties


# --- Example Usage (How to run and test) ---
# To run this service, save the code as a Python file (e.g., main.py).
# Then, open your terminal in the same directory and run:
# pip install "fastapi[all]" pandas # Install FastAPI, Uvicorn, and Pandas
# uvicorn main:app --reload

# Once running, you can access the interactive API documentation at:
# http://127.0.0.1:8000/docs
# Or test the endpoint directly using a URL like:
# http://127.0.0.1:8000/properties/search?roi=0.06&cost=1500000.0  (Area will be ignored)
# http://127.0.0.1:8000/properties/search?area=Business%20Bay (ROI and Cost will be ignored)
# http://127.0.0.1:8000/properties/search (All properties will be returned)
