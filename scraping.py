import pandas as pd
import requests, bs4
from bookdb import BookDB
from decimal import Decimal, ROUND_DOWN

datas = []

#Functionss to loop in one single page from books
def extract_books_page(page):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            return response
        except Exception as e:
            print(f"Status 400 in extract_books: {e}")
            return None
    else:
        print(f"Status 400 in extract_books")
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
        
    df = pd.DataFrame(collected_books)
    return df

#Functions to loop throughout multiple pages from books
def extract_books_pages():
    for i in range(1, 49):        
        response = requests.get(f"http://books.toscrape.com/catalogue/page-{i}.html")
        if response.status_code == 200:
            try:
                datas.append(response)
            except Exception as e:
                print(f"Status 400 in extract_books: {e}")
        else:
            print(f"Status 400 in extract_books")
            
def transform_all_books(responses):
    if datas != []:
        collected_books = {
            "TITLE": [],
            "RATING": [],
            "PRICE": [],
            "IN-STOCK": []
        }
        
        for res in responses:
            soup = bs4.BeautifulSoup(res.text, "lxml")
            books = soup.select(".product_pod")
            
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
            
        df = pd.DataFrame(collected_books)
        return df

#Function to load books into database and CSV file
def load_books_database(books):
    book_db = BookDB()    
    try:
        book_db.databaseConnection()
        book_db.createBookTable()

        for index, row in books.iterrows():
            book = [row['TITLE'], row['RATING'], row['PRICE'], row['IN-STOCK']]
            book_db.addBook(book)

    except Exception as e:
        print(f"An error has happened during load_books_database: {e}")
    
def load_books_csv(books):
    books.to_csv("books.csv", sep=',', index=False, encoding='utf-8')

#Function to only print books on Terminal
def load_books(books):
    for index, row in books.iterrows():
        print(row)