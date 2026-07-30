import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import os

base_url = "http://books.toscrape.com/catalogue/category/books/"

categories = ["travel_2","music_14","art_25","horror_31","history_32","health_47","food-and-drink_33","religion_12"]

all_books = []

for category in categories:
    url = f"{base_url}{category}/index.html"

    while url:

        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, 'html.parser')

        # Actual category name
        breadcrumb = soup.find('ul', class_="breadcrumb")
        category_name = breadcrumb.find_all('li')[-1].get_text(strip=True)  # Home/Books/Travel

        # all books from current page
        books = soup.find_all('article',class_='product_pod')

        for book in books:

            title = book.find('h3').find('a')['title']
            price = book.find('p',class_='price_color').get_text(strip=True)
            star_rating = book.find('p',class_='star-rating')['class'][1]   # ["star-rating", "Three"]
            availability = book.find('p',class_='instock availability').get_text(strip=True)
            book_data = {
                'title':title,
                'price':price,
                'star_rating':star_rating,
                'availability':availability,
                'category':category_name
            }

            all_books.append(book_data)

        next_page = soup.find('li',class_='next')

        if next_page:
            next_url = next_page.find('a')['href']
            url = urljoin(url, next_url)
        else:
            url = None


# save to dataframe


df = pd.DataFrame(all_books)

# Create data folder if it not exist
os.makedirs("data", exist_ok=True)

# Save scraped data to csv
df.to_csv("data/raw_books.csv", index=False)

print("\nTotal books:", len(df))
print("Raw data saved to data/raw_books.csv")