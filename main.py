import scraping


def getAllBooksForDB():
    scraping.extract_books_pages()
    books = scraping.transform_all_books(scraping.datas)
    scraping.load_books_database(books)

def getAllBooksForCSV():
    scraping.extract_books_pages()
    books = scraping.transform_all_books(scraping.datas)
    scraping.load_books_csv(books)

def getAllBooks():
    response = scraping.extract_books_page(2)
    books = scraping.transform_books(response)
    scraping.load_books(books)

