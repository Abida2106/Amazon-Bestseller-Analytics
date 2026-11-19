import json
import pandas as pd

# Read JSON file
with open("dataset/bestsellers.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract book records
books = data["items"]

# Convert into DataFrame
df = pd.DataFrame(books)

# Add category information
df["category"] = data["category"]["name"]
df["category_id"] = data["category"]["node_id"]

# Add data collection timestamp
df["captured_at"] = data["captured_at"]

# Save as CSV
df.to_csv(
    "dataset/bestsellers_2026.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nCSV CREATED SUCCESSFULLY!")

print("\nDataset Preview:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Columns:")
print(df.columns.tolist())