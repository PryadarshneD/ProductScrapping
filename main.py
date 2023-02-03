import requests
from bs4 import BeautifulSoup
import lxml

URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
}

response = requests.get(url=URL, headers=HEADERS)
website = response.text

soup = BeautifulSoup(website, "lxml")

# product url
product_urls = soup.select(selector=".aok-relative a")
urls = [product_url.get("href").strip("javascript:void(0) #").replace("/gp/goldbox/",'') for product_url in product_urls]
all_product_urls = [x for x in urls if x]

# for i in all_product_urls:
#     print(i)

# product names
first_product_names = soup.select(selector=".aok-relative a img")
first_product_names_list = [first_product_name.get("alt").strip("Sponsored Ad -") for first_product_name in
                            first_product_names]

second_product_names = soup.select(selector="span .a-size-medium")
second_product_names_list = [second_product_name.text.strip("Our most functional backpack ever") for second_product_name
                             in second_product_names]

all_product_names = first_product_names_list + second_product_names_list


first_product_prices = soup.select(selector=".a-price-whole")
first_product_prices_list = [first_product_price.text.strip(".") for first_product_price in first_product_prices]

second_product_prices = soup.select(selector=".a-offscreen")
second_product_prices_list = [second_product_price.text.strip("₹") for second_product_price in second_product_prices]

all_product_price = first_product_prices_list + second_product_prices_list

product_ratings = soup.select(selector=".a-icon-alt")
all_product_ratings = [product_rating.text for product_rating in product_ratings]

with open("product_file.csv", "w", encoding="utf-8") as file:
    file.write(f"All product url {all_product_urls}\nAll product names {all_product_names}\nAll product price {all_product_price}\nAll product ratings {all_product_ratings}")

for url in all_product_urls:

    if url[0] != "https":
        URL = f"https://www.amazon.in{url}"

    response = requests.get(url=URL, headers=HEADERS)
    sites = response.text

    soup = BeautifulSoup(sites, "lxml")

    description = soup.select(selector=".a-spacing-mini li span")
    asin = soup.select(selector="#detailBullets_feature_div span span")
    asin_number = [i.text.strip("") for i in asin]
    manu = soup.select(selector="#detailBullets_feature_div span span")
    manufacturer = [i.text.strip("") for i in asin]

print(description)
print(asin_number)
print(manufacturer)

