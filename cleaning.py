import pandas as pd

# Load dataset
df = pd.read_csv("dataset/bestsellers_2026.csv")

print("Original Dataset Shape:", df.shape)

# 1. Remove duplicate records based on ASIN
df = df.drop_duplicates(subset=["asin"])

# 2. Convert date columns into datetime format
date_columns = [
    "first_new_release_at",
    "first_best_seller_at",
    "publication_date",
    "captured_at"
]

for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors="coerce", utc=True)

# 3. Handle missing values
# Keep unavailable numerical values as NaN.
# Do not replace them with zero.

# 4. Check data types
print("\nUpdated Data Types:")
print(df.dtypes)

# 5. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 6. Save cleaned dataset
df.to_csv(
    "dataset/cleaned_bestsellers_2026.csv",
    index=False
)

print("\nData Cleaning Completed!")
print("Cleaned Dataset Shape:", df.shape)
