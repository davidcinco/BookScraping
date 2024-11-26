import scraping

scraping.extract_books_pages()
books = scraping.transform_all_books(scraping.datas)

res = scraping.extract_books_page(2)
dr =scraping.transform_books(res)

scraping.load_books(dr)


