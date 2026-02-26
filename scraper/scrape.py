import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.tayara.tn/ads/c/Immobilier/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_page(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed: {url} — status {response.status_code}")
        return None
    return response.text

def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("article")

    listings = []
    for card in cards:
        try:
            price_tag = card.find("data")
            price = int(price_tag["value"]) if price_tag else None

            title_tag = card.find("h2", class_="card-title")
            title = title_tag.get_text(strip=True) if title_tag else None

            spans = card.find_all("span", class_=lambda c: c and "text-neutral-500" in c)
            category = spans[0].get_text(strip=True) if len(spans) > 0 else None
            location_raw = spans[1].get_text(strip=True) if len(spans) > 1 else None
            location = location_raw.split(",")[0].strip() if location_raw else None

            a_tag = card.find("a", href=True)
            listing_url = "https://www.tayara.tn" + a_tag["href"] if a_tag else None

            listings.append({
                "title": title,
                "price": price,
                "category": category,
                "location": location,
                "url": listing_url
            })

        except Exception as e:
            print(f"Error parsing card: {e}")
            continue

    return listings

def parse_criteria(html):
    """Extract all criteria from an individual listing page."""
    soup = BeautifulSoup(html, "html.parser")
    criteria = {}

    items = soup.find_all("li", class_=lambda c: c and "col-span-6" in c)
    for item in items:
        spans = item.find_all("span")
        if len(spans) >= 2:
            label = spans[0].get_text(strip=True).lower()
            value = spans[1].get_text(strip=True)
            criteria[label] = value

    return criteria

def scrape_all(max_pages=100):
    all_listings = []

    # Step 1: scrape all listing cards
    for page_num in range(1, max_pages + 1):
        print(f"Scraping page {page_num}...")
        html = get_page(f"{BASE_URL}?page={page_num}")

        if html is None:
            break

        listings = parse_listings(html)

        if not listings:
            print(f"No listings on page {page_num} — stopping.")
            break

        all_listings.extend(listings)
        print(f"  → {len(listings)} listings. Total: {len(all_listings)}")
        time.sleep(1.5)

    df = pd.DataFrame(all_listings)

    # Step 2: filter to apartment sales only before hitting individual pages
    # This saves us from scraping hundreds of irrelevant detail pages
    df = df[df['category'] == 'Appartements'].copy()
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df[(df['price'] >= 30_000) & (df['price'] <= 5_000_000)].copy()
    df = df.dropna(subset=['url']).reset_index(drop=True)

    print(f"\nFiltered to {len(df)} apartment sale listings. Now scraping details...")

    # Step 3: visit each listing page and grab criteria
    all_criteria = []
    for i, row in df.iterrows():
        print(f"  Detail page {i+1}/{len(df)}: {row['url']}")
        html = get_page(row['url'])
        if html:
            criteria = parse_criteria(html)
            all_criteria.append(criteria)
        else:
            all_criteria.append({})
        time.sleep(1)

    criteria_df = pd.DataFrame(all_criteria)
    final_df = pd.concat([df.reset_index(drop=True), criteria_df], axis=1)

    return final_df


if __name__ == "__main__":
    print("Starting scraper...")
    df = scrape_all(max_pages=100)

    print(f"\nDone. Final dataset: {df.shape}")
    print(df.head())
    print("\nColumns:", df.columns.tolist())

    df.to_csv("data/raw/listings_with_details.csv", index=False)
    print("Saved to data/raw/listings_with_details.csv") 