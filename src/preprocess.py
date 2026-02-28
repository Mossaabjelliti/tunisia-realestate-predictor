import pandas as pd
import numpy as np
import os

def load_mubawab() -> pd.DataFrame:
    """Load and minimally normalise the mubawab raw CSV so it can be concatenated
    with listings_clean.csv.  All mubawab listings are apartment sales."""
    path = "data/raw/mubawab_listings.csv"
    if not os.path.exists(path):
        print(f"[INFO] {path} not found — skipping mubawab data.")
        return pd.DataFrame()

    mub = pd.read_csv(path)

    # All records from mubawab are sale listings
    mub["transaction_type"] = "vente"

    # Keep only the last part of the location string (city/district)
    mub["location"] = mub["location"].str.split(",").str[-1].str.strip()

    # Select and rename to match listings_clean schema
    mub = mub[["transaction_type", "price", "superficie", "chambres",
               "salles_de_bains", "location", "source"]].copy()

    print(f"[INFO] Mubawab data loaded: {len(mub)} rows")
    return mub


def load_and_clean():
    df_clean = pd.read_csv("data/processed/listings_clean.csv")
    if 'source' not in df_clean.columns:
        df_clean['source'] = 'tayara'
    df_mub = load_mubawab()

    if not df_mub.empty:
        df = pd.concat([df_clean, df_mub], ignore_index=True)
        print(f"[INFO] Combined dataset: {len(df_clean)} + {len(df_mub)} = {len(df)} rows")
    else:
        df = df_clean

    # Keep only sales
    df = df[df['transaction_type'] == 'vente'].copy()

    # Drop rows missing key features
    df = df.dropna(subset=['price', 'superficie', 'chambres', 'location'])

    # Remove garbage superficies
    df = df[(df['superficie'] >= 30) & (df['superficie'] <= 600)]

    # Remove garbage prices
    df = df[(df['price'] >= 30_000) & (df['price'] <= 5_000_000)]

    # Remove garbage chambres
    df = df[(df['chambres'] >= 0) & (df['chambres'] <= 10)]

    # Normalize location — merge rare ones into "Autre"
    top_locations = df['location'].value_counts()
    top_locations = top_locations[top_locations >= 10].index.tolist()
    df['location'] = df['location'].apply(
        lambda x: x if x in top_locations else 'Autre'
    )

    # Feature: price per m²
    df['price_per_sqm'] = df['price'] / df['superficie']

    # Log transform price (reduces skew, helps models)
    df['log_price'] = np.log1p(df['price'])

    print(f"Clean dataset: {df.shape}")
    print(df['location'].value_counts())
    print(df[['price', 'superficie', 'chambres', 'price_per_sqm']].describe())

    df.to_csv("data/processed/listings_final.csv", index=False)
    print("Saved to data/processed/listings_final.csv")

    return df

if __name__ == "__main__":
    load_and_clean()