import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

BASE_URL = "https://www.mubawab.tn/fr/sc/appartements-a-vendre"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.mubawab.tn/",
}


def get_page_url(page_num: int) -> str:
    """Return the correct URL for a given page number."""
    if page_num == 1:
        return BASE_URL
    return f"{BASE_URL}:p:{page_num}"


def get_page(url: str) -> str | None:
    """Fetch a page and return its HTML, or None on failure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            return response.text
        print(f"  [WARN] {url} → HTTP {response.status_code}")
        return None
    except requests.RequestException as e:
        print(f"  [ERROR] {url} → {e}")
        return None


def clean_price(raw: str) -> float | None:
    """
    Convert '406\xa0000 TND' or '406 000 TND' to 406000.0.
    Returns None if parsing fails.
    """
    digits = re.sub(r"[^\d]", "", raw)
    return float(digits) if digits else None


def parse_detail_feature(card: BeautifulSoup, icon_class: str) -> str | None:
    """
    Find the .adDetailFeature whose icon has `icon_class` and return its span text.
    """
    feature = card.find("div", class_="adDetailFeature")
    for feat in card.find_all("div", class_="adDetailFeature"):
        icon = feat.find("i")
        if icon and icon_class in icon.get("class", []):
            span = feat.find("span")
            return span.get_text(strip=True) if span else None
    return None


def extract_number(text: str | None) -> float | None:
    """Pull the first integer/float out of a string like '120 m²' or '3 Chambres'."""
    if not text:
        return None
    m = re.search(r"[\d]+(?:[.,]\d+)?", text)
    return float(m.group().replace(",", ".")) if m else None


def parse_listings(html: str) -> list[dict]:
    """Parse all listing cards from a search-results page."""
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.find_all("div", class_="listingBox")

    listings = []
    for card in cards:
        try:
            # --- URL & ID ---
            url = card.get("linkref") or ""
            ad_id_tag = card.find("input", class_="adId")
            ad_id = ad_id_tag["value"] if ad_id_tag else None

            # --- Price ---
            price_tag = card.find("span", class_="priceTag")
            price_raw = price_tag.get_text(strip=True) if price_tag else None
            price = clean_price(price_raw) if price_raw else None

            # --- Title ---
            title_tag = card.find("h2", class_="listingTit")
            title = title_tag.get_text(strip=True) if title_tag else None

            # --- Location ---
            location_tag = card.find("span", class_="listingH3")
            # The <i class="icon-location"> is empty; get_text() only gives the text nodes
            location_raw = location_tag.get_text(separator=" ", strip=True) if location_tag else None
            # Collapse any embedded whitespace (tabs/newlines between nodes)
            location = re.sub(r"\s+", " ", location_raw).strip() if location_raw else None

            # --- Numeric features from adDetailFeature icons ---
            superficie_txt = parse_detail_feature(card, "icon-triangle")
            superficie = extract_number(superficie_txt)

            pieces_txt = parse_detail_feature(card, "icon-house-boxes")
            pieces = extract_number(pieces_txt)

            chambres_txt = parse_detail_feature(card, "icon-bed")
            chambres = extract_number(chambres_txt)

            sdb_txt = parse_detail_feature(card, "icon-bath")
            salles_de_bains = extract_number(sdb_txt)

            # --- Extra amenity tags ---
            # Live site uses fSize12 (not fSize11 as in sample HTML)
            features = [
                f.find("span").get_text(strip=True)
                for f in card.find_all("div", class_="adFeature")
                if f.find("span") and "extras" not in (f.find("span").get_text() or "")
                and "extraFeatures" not in (f.find("p").get("class", []) if f.find("p") else [])
            ]

            listings.append({
                "ad_id": ad_id,
                "title": title,
                "price": price,
                "location": location,
                "superficie": superficie,
                "pieces": pieces,
                "chambres": chambres,
                "salles_de_bains": salles_de_bains,
                "features": "|".join(features),
                "url": url,
                "source": "mubawab",
            })

        except Exception as e:
            print(f"  [WARN] Error parsing card: {e}")
            continue

    return listings


def scrape_all(max_pages: int = 50, delay: float = 2.0) -> pd.DataFrame:
    """
    Scrape `max_pages` pages of mubawab apartment listings.

    Parameters
    ----------
    max_pages : int
        Maximum number of search-result pages to visit.
    delay : float
        Seconds to wait between requests (be polite to the server).
    """
    all_listings: list[dict] = []

    for page_num in range(1, max_pages + 1):
        url = get_page_url(page_num)
        print(f"[Page {page_num}] {url}")

        html = get_page(url)
        if html is None:
            print("  → Failed to fetch. Stopping.")
            break

        listings = parse_listings(html)
        if not listings:
            print("  → No listings found. Probably past the last page. Stopping.")
            break

        all_listings.extend(listings)
        print(f"  → {len(listings)} listings | total so far: {len(all_listings)}")

        time.sleep(delay)

    df = pd.DataFrame(all_listings)
    if df.empty:
        print("No data scraped.")
        return df

    # Basic cleaning
    df = df.drop_duplicates(subset="ad_id").reset_index(drop=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[
        df["price"].between(10_000, 10_000_000)
    ].reset_index(drop=True)

    # Normalise location to just the city/district name (last part after ", ")
    df["location"] = df["location"].str.split(",").str[-1].str.strip()

    return df


if __name__ == "__main__":
    print("=== Mubawab.tn Apartment Scraper ===")
    df = scrape_all(max_pages=50, delay=2.0)

    if not df.empty:
        print(f"\nDone. Scraped {len(df)} listings.")
        print(df[["title", "price", "location", "superficie", "chambres",
                   "salles_de_bains"]].head(10).to_string())

        out_path = "data/raw/mubawab_listings.csv"
        df.to_csv(out_path, index=False)
        print(f"\nSaved → {out_path}")
    else:
        print("Nothing to save.")
