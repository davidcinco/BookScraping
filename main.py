import scraping

def getAllBooksForCSV():
    scraping.extract_books_pages()
    books = scraping.transform_all_books(scraping.datas)
    scraping.load_books_csv(books)

def getAllBooksForDB():
    scraping.extract_books_pages()
    books = scraping.transform_all_books(scraping.datas)
    scraping.load_books_database(books)
    
