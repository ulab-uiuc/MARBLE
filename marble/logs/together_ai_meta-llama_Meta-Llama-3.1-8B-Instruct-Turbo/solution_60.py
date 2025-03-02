# solution.py

# Importing required libraries
import os
import json
from datetime import datetime

# Class to represent a Book
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.read = False
        self.progress = 0

# Class to represent a Quote
class Quote:
    def __init__(self, text, book):
        self.text = text
        self.book = book

# Class to represent a User Profile
class UserProfile:
    def __init__(self, username):
        self.username = username
        self.bookshelf = []
        self.quotes = []
        self.reviews = {}

# Class to represent the BookVerse Application
class BookVerse:
    def __init__(self):
        self.users = {}

    # Method to add a user to the application
    def add_user(self, username):
        if username not in self.users:
            self.users[username] = UserProfile(username)
            print(f"User {username} added successfully.")
        else:
            print(f"User {username} already exists.")

    # Method to search for quotes by book title, author, or keyword
    def search_quotes(self, username, query):
        if username in self.users:
            user = self.users[username]
            results = []
            for quote in user.quotes:
                if query.lower() in quote.text.lower() or query.lower() in quote.book.title.lower() or query.lower() in quote.book.author.lower():
                    results.append(quote)
            return results
        else:
            print("User not found.")

    # Method to save a quote to the user's profile
    def save_quote(self, username, text, book_title, book_author):
        if username in self.users:
            user = self.users[username]
            quote = Quote(text, Book(book_title, book_author, 0))
            user.quotes.append(quote)
            print(f"Quote saved successfully.")
        else:
            print("User not found.")

    # Method to add a book to the user's bookshelf
    def add_book(self, username, title, author, pages):
        if username in self.users:
            user = self.users[username]
            book = Book(title, author, pages)
            user.bookshelf.append(book)
            print(f"Book added to bookshelf successfully.")
        else:
            print("User not found.")

    # Method to update the user's reading progress
    def update_progress(self, username, book_title, progress):
        if username in self.users:
            user = self.users[username]
            for book in user.bookshelf:
                if book.title == book_title:
                    book.progress = progress
                    print(f"Progress updated successfully.")
                    return
            print("Book not found in bookshelf.")
        else:
            print("User not found.")

    # Method to mark a book as read
    def mark_book_as_read(self, username, book_title):
        if username in self.users:
            user = self.users[username]
            for book in user.bookshelf:
                if book.title == book_title:
                    book.read = True
                    print(f"Book marked as read successfully.")
                    return
            print("Book not found in bookshelf.")
        else:
            print("User not found.")

    # Method to write a review for a book
    def write_review(self, username, book_title, review):
        if username in self.users:
            user = self.users[username]
            user.reviews[book_title] = review
            print(f"Review written successfully.")
        else:
            print("User not found.")

    # Method to display the user's bookshelf
    def display_bookshelf(self, username):
        if username in self.users:
            user = self.users[username]
            print("Bookshelf:")
            for book in user.bookshelf:
                print(f"Title: {book.title}, Author: {book.author}, Pages: {book.pages}, Progress: {book.progress}, Read: {book.read}")
        else:
            print("User not found.")

    # Method to display the user's quotes
    def display_quotes(self, username):
        if username in self.users:
            user = self.users[username]
            print("Quotes:")
            for quote in user.quotes:
                print(f"Text: {quote.text}, Book: {quote.book.title} by {quote.book.author}")
        else:
            print("User not found.")

    # Method to display the user's reviews
    def display_reviews(self, username):
        if username in self.users:
            user = self.users[username]
            print("Reviews:")
            for book, review in user.reviews.items():
                print(f"Book: {book}, Review: {review}")
        else:
            print("User not found.")

# Main function
def main():
    bookverse = BookVerse()

    while True:
        print("\nBookVerse Menu:")
        print("1. Add User")
        print("2. Search Quotes")
        print("3. Save Quote")
        print("4. Add Book")
        print("5. Update Progress")
        print("6. Mark Book as Read")
        print("7. Write Review")
        print("8. Display Bookshelf")
        print("9. Display Quotes")
        print("10. Display Reviews")
        print("11. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            bookverse.add_user(username)
        elif choice == "2":
            username = input("Enter username: ")
            query = input("Enter search query: ")
            results = bookverse.search_quotes(username, query)
            if results:
                print("Search results:")
                for result in results:
                    print(f"Text: {result.text}, Book: {result.book.title} by {result.book.author}")
            else:
                print("No results found.")
        elif choice == "3":
            username = input("Enter username: ")
            text = input("Enter quote text: ")
            book_title = input("Enter book title: ")
            book_author = input("Enter book author: ")
            bookverse.save_quote(username, text, book_title, book_author)
        elif choice == "4":
            username = input("Enter username: ")
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            pages = int(input("Enter number of pages: "))
            bookverse.add_book(username, title, author, pages)
        elif choice == "5":
            username = input("Enter username: ")
            book_title = input("Enter book title: ")
            progress = int(input("Enter progress: "))
            bookverse.update_progress(username, book_title, progress)
        elif choice == "6":
            username = input("Enter username: ")
            book_title = input("Enter book title: ")
            bookverse.mark_book_as_read(username, book_title)
        elif choice == "7":
            username = input("Enter username: ")
            book_title = input("Enter book title: ")
            review = input("Enter review: ")
            bookverse.write_review(username, book_title, review)
        elif choice == "8":
            username = input("Enter username: ")
            bookverse.display_bookshelf(username)
        elif choice == "9":
            username = input("Enter username: ")
            bookverse.display_quotes(username)
        elif choice == "10":
            username = input("Enter username: ")
            bookverse.display_reviews(username)
        elif choice == "11":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()