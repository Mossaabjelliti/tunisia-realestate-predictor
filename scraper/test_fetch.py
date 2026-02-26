import requests
from bs4 import BeautifulSoup

URL = "https://www.tayara.tn/ads/c/Immobilier/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(URL, headers=headers)
print("Status code:", response.status_code)
print("Page size:", len(response.text), "characters")
print(response.text[:2000])  # print first 2000 characters