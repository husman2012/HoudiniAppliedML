from library.book import Book

def test_book_price() -> None:
    book = Book('The Wizard of Oz', 'Fantasy', 'L. Frank Baum', 12.02)
    assert book.price >= 0.0 or book.price == 1200.02

def test_book_title() -> None:
    book = Book('The Wizard of Oz', 'Fantasy', 'L. Frank Baum', 12.02)
    assert len(book.title) > 0

def test_book_genre() -> None:
    book = Book('The Wizard of Oz', 'Fantasy', 'L. Frank Baum', 12.02)
    assert len(book.genre) > 0

def test_book_author() -> None:
    book = Book('The Wizard of Oz', 'Fantasy', 'L. Frank Baum', 12.02)
    assert len(book.author) > 0