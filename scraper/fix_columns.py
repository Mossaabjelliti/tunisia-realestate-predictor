import pandas as pd
import re

df = pd.read_csv("data/raw/listings_with_details.csv")

# The columns we actually want to extract
base_columns = ['title', 'price', 'category', 'location', 'url']
result = df[base_columns].copy()

# For each row, reconstruct superficie, chambres, salles de bains, transaction type
# by finding which of the 167 columns is NOT null for that row

def extract_field(row, prefix):
    """Find the column starting with prefix that has a value for this row."""
    for col in df.columns:
        if col.startswith(prefix) and pd.notna(row[col]):
            # Extract the numeric part from the column name
            value = col.replace(prefix, "").strip()
            return value
    return None

print("Extracting fields from column names...")

result['transaction_type'] = df.apply(
    lambda row: 'vente' if pd.notna(row.get('type de transactionà vendre')) 
    else ('louer' if pd.notna(row.get('type de transactionà louer')) else None), 
    axis=1
)

result['superficie'] = df.apply(lambda row: extract_field(row, 'superficie'), axis=1)
result['chambres'] = df.apply(lambda row: extract_field(row, 'chambres'), axis=1)
result['salles_de_bains'] = df.apply(lambda row: extract_field(row, 'salles de bains'), axis=1)

# Convert to numeric
result['superficie'] = pd.to_numeric(result['superficie'], errors='coerce')
result['chambres'] = pd.to_numeric(result['chambres'], errors='coerce')
result['salles_de_bains'] = pd.to_numeric(result['salles_de_bains'], errors='coerce')

# Normalize location
result['location'] = result['location'].str.strip().str.title()

print(result.shape)
print(result.head(10).to_string())
print("\nMissing values:")
print(result.isnull().sum())
print("\nTransaction types:")
print(result['transaction_type'].value_counts())
print("\nSuperficie stats:")
print(result['superficie'].describe())

result.to_csv("data/processed/listings_clean.csv", index=False)
print("\nSaved to data/processed/listings_clean.csv")