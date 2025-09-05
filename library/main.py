from library.library import Library
from library.book import Book

if __name__ == "__main__":

    #The main database for the library
    database = "./database.json"
    my_library = Library(database)

    #Search for an item
    print("Searching for item...")
    search_query = "The Wizard of Oz"
    found_items = my_library.search_books(search_query)
    print('--------------------------')

    #get the total amount of items in the library
    print("Total items in library:", my_library.get_total_book_count())
    print('--------------------------')

    #Create a Book object and add it to the library
    print("Adding book to library...")
    book1 = Book(title="Fahrenheit 451", genre="Dystopian", author="Ray Bradbury", _price=3.49)
    my_library.add_book_to_library(book1)
    book2 = Book(title="Oliver Twist", genre="Victorian", author="Charles Dickens", _price=0.99)
    my_library.add_book_to_library(book2)
    print('--------------------------')

    #Get all items in the library
    print("Getting all books in library...")
    all_items = my_library.get_all_books()
    print("--------------------------")

    #remove all items by name or type
    print('Removing all instances of an item from library..')
    print('--------------------------')
    my_library.remove_books_from_library_by_query("Fahrenheit 451")
    print('--------------------------')
    print('\n')

    #Removes a selected item
    print('Removing a specific item by selection')
    print('--------------------------')
    my_library.remove_book_from_library_by_selection()
    print('--------------------------')

    print('All the current books in the library:')
    my_library.print_all_books(verbose=1)
    print('--------------------------')

    print('Total Price of all books in the library:')
    total_price = my_library.get_total_price()
