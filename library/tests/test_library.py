import pytest
from library.library import Library
from library.book import Book

@pytest.fixture
def library():
    database = './tests/test_database.json'
    library = Library(database)
    library.empty_library()
    return library

def test_total_price_of_library(library):
    book1 = Book('The Wizard of Oz', 'fantasy', 'L. Frank Baum', 2.0)
    book2 = Book('1984', 'dystopian', 'George Orwell', 3.5)
    library.add_book_to_library(book1)
    library.add_book_to_library(book2)
    assert library.get_total_price() == 5.5

def test_empty_library(library):
    book1 = Book('To Kill a Mockingbird', 'fiction', 'Harper Lee', 4.0)
    library.add_book_to_library(book1)
    library.empty_library()
    assert library.get_total_book_count() == 0

def test_search_item(library):
    book = Book('The Great Gatsby', 'fiction', 'F. Scott Fitzgerald', 2.5)
    library.add_book_to_library(book)
    books_list = library.search_books('The Great Gatsby')
    assert books_list[0].title == 'The Great Gatsby'

def test_get_all_items(library):
    book1 = Book('The Wizard of Oz', 'fantasy', 'L. Frank Baum', 2.0)
    book2 = Book('1984', 'dystopian', 'George Orwell', 3.5)
    library.add_book_to_library(book1)
    library.add_book_to_library(book2)
    retrieved_items = library.get_all_books()
    names_to_compare = [book1.title, book2.title]
    results = [book_data['title'] for book_id, book_data in retrieved_items['Items'].items()]
    assert names_to_compare == results

def test_get_total_item_count(library):
    book1 = Book('The Wizard of Oz', 'fantasy', 'L. Frank Baum', 2.0)
    book2 = Book('1984', 'dystopian', 'George Orwell', 3.5)
    library.add_book_to_library(book1)
    library.add_book_to_library(book2)
    assert library.get_total_book_count() == 2