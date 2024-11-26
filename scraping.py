import pandas as pd
import requests, bs4
from decimal import Decimal, ROUND_DOWN
from bookdb import BookDB

website_url = f"http://books.toscrape.com/catalogue/page-30.html"

def extract_books(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response
        except Exception as e:
            print(f"Status 400 in extract_books: {e}")
            return None
    else:
        print(f"Status 400 in extract_books: {e}")
        return None

def transform_books(datas):
    soup = bs4.BeautifulSoup(datas.text, "lxml")
    books = soup.select(".product_pod")

    collected_books = {
        "TITLE": [],
        "RATING": [],
        "PRICE": [],
        "IN-STOCK": []
    }
    
    for book in books:
        #Book's Title 
        title = book.h3.a['title']        
        #Book's Rating
        if book.select_one(".One"):
            rate = 1
        elif book.select_one(".Two"):
            rate = 2
        elif book.select_one(".Three"):
            rate = 3
        elif book.select_one(".Four"):
            rate = 4
        elif book.select_one(".Five"):
            rate = 5
        else:
            rate = None

        #Price
        data_price = book.select('.price_color')[0].getText()
        price_split = data_price.split("Â")
        price = Decimal(price_split[1].split("£")[1]).quantize(Decimal("0.00"), rounding=ROUND_DOWN)
                
        #Stock Available
        #strip method to remove start and end whitespace
        stock_available = book.select('.instock')[0].getText().strip()
        if stock_available == "In stock":
            stock = True
        else:
            stock = False

        collected_books['TITLE'].append(title)
        collected_books['RATING'].append(rate)
        collected_books['PRICE'].append(price)
        collected_books['IN-STOCK'].append(stock)
        
        # book_to_store = {
        #  "title": title, "rating": rate,
        #  "price": price, "stock": stock 
        # }
        
        # collected_books.append(book_to_store)

    df = pd.DataFrame(collected_books)
    return df

# def load_books(books):

extract = extract_books(website_url)
if extract is not None:
    transform = transform_books(extract)
    print(transform)