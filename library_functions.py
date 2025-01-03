import json
import re
from datetime import datetime

BookCatalog = []

def add_new_book():
    print("=== Add New Book ===")
    try:
         # Prompt user for book details
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        isbn = input("Enter ISBN (format: XXX-X-XX-XXXXXX-X): ")
        year = input("Enter publication year: ")

        # Validate inputs
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if not author.strip():
            raise ValueError("Author cannot be empty")
        isbn_pattern = r"^\d{3}-\d-\d{2}-\d{6}-\d$"
        if not re.match(isbn_pattern, isbn):
            raise ValueError("Invalid ISBN format")
        if not year.isdigit() or not (1000 <= int(year) <= datetime.now().year):
            raise ValueError("Invalid publication year")

        # Set initial book status
        status = "Available"
        borrower = None
        borrowed_date = None
        added_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the new book to the book catalog
        book = {
            "Title": title,
            "Author": author,
            "ISBN": isbn,
            "Year": int(year),
            "Status": status,
            "Borrower": borrower,
            "BorrowedDate": borrowed_date,
            "AddedDate": added_date,
        }
        BookCatalog.append(book)

        print("Book added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def remove_book():
    try:
        isbn = input("Enter ISBN to remove: ").strip()
        book_to_remove = next((book for book in BookCatalog if book["ISBN"] == isbn), None)
        if not book_to_remove:
            raise ValueError("Book not found.")
        
        BookCatalog.remove(book_to_remove)
        print("Book removed successfully.")
    except ValueError as e:
        print(e)

def update_book():
    try:
        isbn = input("Enter ISBN of the book to update: ").strip()
        book_to_update = next((book for book in BookCatalog if book["ISBN"] == isbn), None)
        if not book_to_update:
            raise ValueError("Book not found.")
        
        title = input("Enter new title: ").strip()
        author = input("Enter new author: ").strip()
        year = input("Enter new publication year: ").strip()

        # Validate inputs
        if not title:
            raise ValueError("Title cannot be empty")
        if not author:
            raise ValueError("Author cannot be empty")
        if not year.isdigit() or not (1000 <= int(year) <= datetime.now().year):
            raise ValueError("Invalid publication year")

        book_to_update.update({
            "Title": title,
            "Author": author,
            "Year": int(year)
        })
        print("Book updated successfully.")
    except ValueError as e:
        print(e)

def search_books():
    try:
        criteria = input("Search by title/author/ISBN/year: ").lower().strip()
        results = [
            book for book in BookCatalog
            if criteria in book["Title"].lower() or
               criteria in book["Author"].lower() or
               criteria in str(book["Year"]) or
               criteria in book["ISBN"]
        ]
        if not results:
            raise ValueError("No books found.")
        for book in results:
            print(book)

            
    except ValueError as e:
        print(e)

def borrow_book():
    try:
        isbn = input("Enter ISBN to borrow: ").strip()
        book_to_borrow = next((book for book in BookCatalog if book["ISBN"] == isbn), None)
        if not book_to_borrow:
            raise ValueError("Book not found.")
        if book_to_borrow["Status"] != "Available":
            raise ValueError("Book not available for borrowing.")
        
        borrower = input("Enter borrower name: ").strip()
        book_to_borrow.update({
            "Status": "Borrowed",
            "Borrower": borrower,
            "BorrowedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        print(f"Book '{book_to_borrow['Title']}' borrowed by {borrower}.")
    except ValueError as e:
        print(e)

def return_book():
    try:
        isbn = input("Enter ISBN to return: ").strip()
        book_to_return = next((book for book in BookCatalog if book["ISBN"] == isbn), None)
        if not book_to_return:
            raise ValueError("Book not found.")
        if book_to_return["Status"] != "Borrowed":
            raise ValueError("Book not borrowed or already returned.")
        
        book_to_return.update({
            "Status": "Available",
            "Borrower": None,
            "BorrowedDate": None
        })
        print(f"Book '{book_to_return['Title']}' returned successfully.")
    except ValueError as e:
        print(e)
        
def list_all_books():
    """
    Lists all the books in the BookCatalog.
    """
    print("\n=== List of All Books ===")
    if not BookCatalog:
        print("No books available in the catalog.")
        return

    for i, book in enumerate(BookCatalog, 1):
        print(f"\nBook {i}:")
        print(f"  Title: {book['Title']}")
        print(f"  Author: {book['Author']}")
        print(f"  ISBN: {book['ISBN']}")
        print(f"  Year: {book['Year']}")
        print(f"  Status: {book['Status']}")
        if book['Status'] == "Borrowed":
            print(f"  Borrower: {book['Borrower']}")
            print(f"  Borrowed Date: {book['BorrowedDate']}")
        print(f"  Added Date: {book['AddedDate']}")

def view_stats():
    total_books = len(BookCatalog)
    available_books = sum(1 for book in BookCatalog if book["Status"] == "Available")
    borrowed_books = total_books - available_books

    print(f"\nLibrary Statistics:")
    print(f"Total books: {total_books}")
    print(f"Available books: {available_books}")
    print(f"Borrowed books: {borrowed_books}")

def save_data():
    try:
        with open("library_data.json", "w") as f:
            json.dump(BookCatalog, f)
    except IOError as e:
        print(f"Error saving data: {e}")

def load_data():
    global BookCatalog
    try:
        with open("library_data.json", "r") as f:
            BookCatalog = json.load(f)
    except FileNotFoundError:
        print("No previous data found.")
    except IOError as e:
        print(f"Error loading data: {e}")

def main_menu():
    load_data()
    while True:
        print("\nLibrary Book Tracking System Menu:")
        print("1. Add New Book")
        print("2. Remove Book")
        print("3. Update Book")
        print("4. Search")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. View Stats")
        print("8. List All Books")
        print("9. Exit")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            add_new_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            update_book()
        elif choice == '4':
            search_books()
        elif choice == '5':
            borrow_book()
        elif choice == '6':
            return_book()
        elif choice == '7':
            view_stats()
        elif choice == '8':
            list_all_books()
        elif choice == '9':
            save_data()
            print("Exiting the system...")
            break
        else:
            print("Invalid choice. Please try again.")
