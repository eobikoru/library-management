import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from library_functions import add_new_book, remove_book, update_book


class TestBookCatalog(unittest.TestCase):

    def setUp(self):
        """Set up the test environment before each test case."""
        global BookCatalog
        BookCatalog = []  # Reset the catalog before each test

    @patch("builtins.input", side_effect=["Test Book", "Author Name", "123-4-56-789012-3", "2023"])
    def test_add_new_book_valid(self, mock_input):
        add_new_book()
        self.assertEqual(len(BookCatalog), 1)
        book = BookCatalog[0]
        self.assertEqual(book["Title"], "Test Book")
        self.assertEqual(book["Author"], "Author Name")
        self.assertEqual(book["ISBN"], "123-4-56-789012-3")
        self.assertEqual(book["Year"], 2023)
        self.assertEqual(book["Status"], "Available")

    @patch("builtins.input", side_effect=["", "Author Name", "123-4-56-789012-3", "2023"])
    def test_add_new_book_invalid_title(self, mock_input):
        with patch("builtins.print") as mock_print:
            add_new_book()
            mock_print.assert_called_with("Error: Title cannot be empty")

    @patch("builtins.input", side_effect=["123-4-56-789012-3"])
    def test_remove_book_valid(self, mock_input):
        BookCatalog.append({
            "Title": "Test Book",
            "Author": "Author Name",
            "ISBN": "123-4-56-789012-3",
            "Year": 2023,
            "Status": "Available",
            "Borrower": None,
            "BorrowedDate": None,
            "AddedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        remove_book()
        self.assertEqual(len(BookCatalog), 0)

    @patch("builtins.input", side_effect=["000-0-00-000000-0"])
    def test_remove_book_not_found(self, mock_input):
        with patch("builtins.print") as mock_print:
            remove_book()
            mock_print.assert_called_with("Book not found.")

    @patch("builtins.input", side_effect=["123-4-56-789012-3", "Updated Book", "Updated Author", "2022"])
    def test_update_book_valid(self, mock_input):
        BookCatalog.append({
            "Title": "Test Book",
            "Author": "Author Name",
            "ISBN": "123-4-56-789012-3",
            "Year": 2023,
            "Status": "Available",
            "Borrower": None,
            "BorrowedDate": None,
            "AddedDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        update_book()
        self.assertEqual(BookCatalog[0]["Title"], "Updated Book")
        self.assertEqual(BookCatalog[0]["Author"], "Updated Author")
        self.assertEqual(BookCatalog[0]["Year"], 2022)

if __name__ == "__main__":
    unittest.main()