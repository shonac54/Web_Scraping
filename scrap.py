import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=phone+covers"  # Modified URL for phone covers

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except requests.RequestException as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
cover_cards = soup.find_all("div", class_="s-result-item")

cover_data = []

for cover_card in cover_cards:
    try:
        cover_name = cover_card.find("span", class_="a-text-normal").text.strip()
        cover_price = cover_card.find("span", class_="a-offscreen").text if cover_card.find("span", class_="a-offscreen") else "N/A"
        cover_rating = cover_card.find("span", class_="a-icon-alt").text if cover_card.find("span", class_="a-icon-alt") else "N/A"
        
        cover_data.append({
            "Name": cover_name,
            "Price": cover_price,
            "Rating": cover_rating
        })
    except Exception as e:
        print("Error in extracting cover data:", e)

df = pd.DataFrame(cover_data)
df.to_csv("amazon_phone_covers.csv", index=False)

print("Data successfully extracted and CSV saved for phone covers.")
