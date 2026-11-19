import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned dataset
df = pd.read_csv("dataset/cleaned_bestsellers_2026.csv")

# Create charts folder if it doesn't exist
os.makedirs("charts", exist_ok=True)


# 1. Top 10 Books by Bestseller Rank
plt.figure(figsize=(12, 6))

plt.barh(df["title"], df["rank"])

plt.xlabel("Bestseller Rank")
plt.ylabel("Book Title")
plt.title("Top 10 Amazon Bestselling Books")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("charts/top_10_books.png")
plt.show()


# 2. Book Ratings
plt.figure(figsize=(10, 5))

plt.bar(df["title"], df["rating"])

plt.xlabel("Book Title")
plt.ylabel("Rating")
plt.title("Ratings of Amazon Bestselling Books")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("charts/book_ratings.png")
plt.show()


# 3. Book Price Distribution
plt.figure(figsize=(8, 5))

plt.hist(df["price"], bins=5)

plt.xlabel("Price ($)")
plt.ylabel("Number of Books")
plt.title("Distribution of Book Prices")

plt.tight_layout()
plt.savefig("charts/book_prices.png")
plt.show()


# 4. Book Format Distribution
plt.figure(figsize=(8, 6))

format_counts = df["format"].value_counts()

plt.pie(
    format_counts,
    labels=format_counts.index,
    autopct="%1.1f%%"
)

plt.title("Distribution of Book Formats")

plt.savefig("charts/book_formats.png")
plt.show()


# 5. Reviews vs Ratings
plt.figure(figsize=(8, 5))

plt.scatter(df["review_count"], df["rating"])

plt.xlabel("Number of Reviews")
plt.ylabel("Rating")
plt.title("Reviews vs Book Ratings")

plt.tight_layout()
plt.savefig("charts/reviews_vs_ratings.png")
plt.show()


print("\nAll visualizations created successfully!")
