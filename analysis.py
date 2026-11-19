import pandas as pd

# Load dataset
df = pd.read_csv("dataset/bestsellers_2026.csv")

# 1. Display first five records
print("\n--- DATASET PREVIEW ---")
print(df.head())

# 2. Dataset information
print("\n--- DATASET INFORMATION ---")
print(df.info())

# 3. Dataset dimensions
print("\n--- DATASET SHAPE ---")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# 4. Check missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 5. Check duplicate records
print("\n--- DUPLICATE RECORDS ---")
print(df.duplicated().sum())

# 6. Statistical summary
print("\n--- DESCRIPTIVE STATISTICS ---")
print(df.describe())

# 7. Unique authors
print("\n--- UNIQUE AUTHORS ---")
print(df["author"].nunique())

# 8. Book formats
print("\n--- BOOK FORMATS ---")
print(df["format"].value_counts())
