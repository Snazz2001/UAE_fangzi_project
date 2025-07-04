import pandas as pd
from typing import Dict, Optional
from pathlib import Path

# Simulate user preferences. In a real application, this would come from a database,
# user profiles, or be inferred from past behavior.
# Each user has a dictionary of preferences. 'None' means the user has no preference for that criterion.
user_preferences: Dict[int, Dict[str, Optional[str | float]]] = {
    101: {"area": "Business Bay", "max_cost": 1600000.0, "min_roi": 0.07},
    102: {"area": "Downtown Dubai", "max_cost": 6000000.0, "min_roi": 0.04},
    103: {"area": "Arabian Ranches", "max_cost": 3500000.0, "min_roi": 0.05},
    104: {"area": None, "max_cost": 1000000.0, "min_roi": 0.07}, # User 104 doesn't care about area
    105: {"area": "JLT", "max_cost": 2500000.0, "min_roi": 0.07},
    106: {"area": "Business Bay", "max_cost": None, "min_roi": 0.06}, # User 106 doesn't care about max cost
    107: {"area": None, "max_cost": None, "min_roi": None}, # User 107 has no specific preferences
}

def recommend_properties(user_id: int, properties_df: pd.DataFrame) -> pd.DataFrame:
    """
    Recommends properties based on a given user's preferences.

    Args:
        user_id (int): The ID of the user for whom to generate recommendations.
        properties_df (pd.DataFrame): A DataFrame containing property data.
                                      Expected columns: 'area', 'cost', 'expected_roi'.

    Returns:
        pd.DataFrame: A DataFrame containing properties recommended for the user.
                      Returns an empty DataFrame if no preferences found for user_id
                      or no properties match.
    """
    if user_id not in user_preferences:
        print(f"Error: No preferences found for user ID {user_id}.")
        return pd.DataFrame(columns=properties_df.columns)

    user_pref = user_preferences[user_id]
    
    # Start with all properties
    recommended_df = properties_df.copy()

    # Apply area filter if specified
    if user_pref.get("area"):
        # Convert both to lowercase for case-insensitive comparison
        preferred_area_lower = str(user_pref["area"]).lower()
        recommended_df = recommended_df[
            recommended_df["area"].str.lower() == preferred_area_lower
        ]

    # Apply maximum cost filter if specified
    if user_pref.get("max_cost") is not None:
        recommended_df = recommended_df[
            recommended_df["cost"] <= user_pref["max_cost"]
        ]

    # Apply minimum ROI filter if specified
    if user_pref.get("min_roi") is not None:
        recommended_df = recommended_df[
            recommended_df["expected_roi"] >= user_pref["min_roi"]
        ]

    return recommended_df

def main(repo_path: str) -> pd.DataFrame:
    """
    Main function to load properties and recommend based on user preferences.

    Args:
        repo_path (str): Path to the CSV file containing property data.

    Returns:
        pd.DataFrame: DataFrame of all properties loaded from the CSV.
    """
    # Load the CSV content into a DataFrame
    file_path = repo_path / "data/properties_2025_07_04.csv"
    properties_df = pd.read_csv(file_path)

    print("\n" + "="*40 + "\n")
    print("--- All Properties ---")
    print(properties_df)
    print("\n" + "="*40 + "\n")

    # Ensure the DataFrame has the expected columns
    expected_columns = {"area", "cost", "expected_roi"}
    if not expected_columns.issubset(properties_df.columns):
        raise ValueError(f"CSV file must contain columns: {expected_columns}")
    
    user_id_1 = 101
    recommendations_1 = recommend_properties(user_id_1, properties_df)
    print(f"--- Recommendations for User {user_id_1} (Business Bay, max 1.6M, min 6% ROI) ---")
    if not recommendations_1.empty:
        print(recommendations_1)
        recommendations_1.to_csv(repo_path / f"data/recommendations_user_{user_id_1}.csv", index=False)
    else:
        print("No properties found matching criteria.")


    return properties_df

# --- Example Usage ---
if __name__ == "__main__":
    # Load the CSV content into a DataFrame
    properties_df = main(Path("/workspaces/anaconda"))

# Add dvc pipeline
'''dvc stage add --name recommend --deps recommend_property_by_user.py --deps data/properties_2025_07_04.csv --outs data/recommendations_user_101.csv python recommend_property_by_user.py '''