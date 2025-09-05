import json
from dataclasses import dataclass, field
from library.book import Book 
from library.random_number_utils import RandomUtils
from library.file_io import Fstream

@dataclass
class Library:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init = False, default_factory = RandomUtils.generate_random_id)
    
    def get_all_books(self, verbose = False) -> dict:
        """
        Reads and returns a hash map with all available books

        Args:
            verbose: If true, prints all books to console
        Returns:
            dict: A hash map with all books in database
        """
        data_file = Fstream.load_json_files(self.database_path)
        
        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        if verbose:
            Fstream.print_json_structure(data_file)
    
        return data_file

    def search_books(self, query: str) -> list[Book]:
        """
        Searches for books in the database that match the query string

        Args:
            query: The search string
        Returns:
            list[Book]: A list of books that match the search string
        """
        data_file = Fstream.load_json_files(self.database_path)
        
        results = []

        for id, item in data_file['Items'].items():
            current_item = Book(title=item['title'], genre=item['genre'], author=item['author'], _price=item['price'], id=id)
            if query.lower() in current_item.search_string.lower():
                results.append(current_item)
        
        if len(results) == 0:
            print(f"No books found matching '{query}'")
        else:
            print(f"Found {len(results)} books matching '{query}':")
            for book in results:
                print(f" - {book.title}, {book.author} ({book.genre}): ${book.price}")

        return results

    def get_total_book_count(self) -> int:
        """
        Gets the total number of books in the library

        Returns:
            int: The total number of books
        """
        data = self.get_all_books()
        return len(data['Items'].items())

    def add_book_to_library(self, book: Book) -> None:
        """
        Adds a book to the library

        Args:
            book: The book to add
        Returns:
            None
        """
        data = self.get_all_books()
        new_item = {
            "title": book.title,
            "genre": book.genre,
            "author": book.author,
            "price": book.price
        }

        data['Items'][book.id] = new_item

        with open(self.database_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.isEmpty = False
        self.isActive = True

        print(f"Added book '{book.title}' to library.")

    def remove_books_from_library_by_query(self, query: str) -> None:
        """
        Removes a book from the library by a search query

        Args:
            query: The search string to find the book to remove
        Returns:
            None
        """
        data = self.get_all_books()

        books_to_remove = []

        for book_id, book_data in data['Items'].items():
            if query.lower() in book_data['title'].lower() or query.lower() in book_data['author'].lower() or query.lower() in book_data['genre'].lower():
                books_to_remove.append(book_id)

        if not books_to_remove:
            print(f"No books found matching '{query}' to remove.")
            return

        for book_id in books_to_remove:
            book_title = data['Items'][book_id]['title']
            del data['Items'][book_id]
            print(f"Removed book '{book_title}' from library.")

        with open(self.database_path, 'w') as f:
            json.dump(data, f, indent=4)

        if not data['Items']:
            self.isEmpty = True
            self.isActive = False

    def get_total_price(self) -> float:
        """
        Gets the total price of all books in the cart
        
        Returns:
            float: The total price of all books
        """
        data = self.get_all_books()
        total_price = 0.0

        for book_id, book_data in data['Items'].items():
            total_price += book_data['price']

        return round(total_price, 2)
    
    def remove_book_from_library_by_selection(self) -> None:
        """
        Removes the selected book by index based on user input
        Returns:
            None
        """

        data = self.get_all_books()
        books = []

        i = 1
        for book_id, book_data in data['Items'].items():
            books.append((book_id, book_data))
            
            print(f"{i}. {book_data['title']} ({book_data['author']}): ${book_data['price']}")
            i += 1
        selection = input("Enter the number of the book to remove (or 'q' to cancel): ")

        if selection.lower() == 'q':
            print("Removal canceled.")
            return

        try:
            selected_index = int(selection) - 1
            if 0 <= selected_index < len(books):
                book_id, book_data = books[selected_index]
                del data['Items'][book_id]
                print(f"Removed book '{book_data['title']}' from cart.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

        with open(self.database_path, 'w') as f:
            json.dump(data, f, indent=4)

        if not data['Items']:
            self.isEmpty = True
            self.isActive = False

    def print_all_books(self, verbose = False) -> None:
        """
        Prints all books in the library

        Args:
            verbose: If true, prints all books to console
        Returns:
            None
        """
        self.get_all_books(verbose)

    def empty_library(self) -> None:
        """
        Empties the library by removing all books

        Returns:
            None
        """
        data = {
            "Items": {}
        }

        with open(self.database_path, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.isEmpty = True
        self.isActive = False

        print("Emptied the library.")
