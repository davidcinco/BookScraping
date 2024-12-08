import pytest, requests
from scraping import extract_books_page, extract_books_pages

def test_extract_books_page():
    data = extract_books_page(1)
    assert data == requests.status_codes.codes.ok
    
# def test_extract_books_pages():
#     assert extract_books_pages()
