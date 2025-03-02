
from collections import defaultdict

class BookVerse:
    # ... existing code ...
    def search_quotes(self, keyword):
        quotes = defaultdict(list)
        for user in self.users.values():
            for quote in user.quotes:
                quotes[quote.book.title].append(quote)
        return quotes.get(keyword, [])# solution.py

# Importing required libraries
import os
import getpass
import datetime
import random

# Class to represent a Book
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.read = False
        self.progress = 0

    def mark_as_read(self):
        self.read = True

    def update_progress(self, progress):
        self.progress = progress

# Class to represent a Quote
class Quote:
    def __init__(self, text, book):
        self.text = text
        self.book = book

    def save_quote(self):
        print(f"Quote saved: {self.text} - {self.book.title} by {self.book.author}")

    def share_quote(self):
        print(f"Sharing quote: {self.text} - {self.book.title} by {self.book.author}")

# Class to represent a User Profile
class UserProfile:
    def __init__(self, username):
        self.username = username
        self.bookshelf = []
        self.quotes = []

    def add_book(self, book):
        self.bookshelf.append(book)

    def remove_book(self, book):
        self.bookshelf.remove(book)

    def view_bookshelf(self):
        for book in self.bookshelf:
            print(f"{book.title} by {book.author}")

    def view_quotes(self):
        for quote in self.quotes:
            print(f"{quote.text} - {quote.book.title} by {quote.book.author}")

# Class to represent the BookVerse Application
class BookVerse:
    def __init__(self):
        self.users = {}

    def create_user(self, username):
        if username not in self.users:
self.users[username] = UserProfile(username)
print(f"User created: {username}")
            self.users[username] = UserProfile(username)
            print(f"User created: {username}")
        else:
            print(f"User already exists: {username}")

    def login_user(self, username):
        if username in self.users:
            print(f"User logged in: {username}")
            return self.users[username]
        else:
            print(f"User does not exist: {username}")
            return None

    def search_quotes(self, keyword):
        quotes = []
        for user in self.users.values():
            for quote in user.quotes:
                if keyword in quote.text or keyword in quote.book.title or keyword in quote.book.author:
                    quotes.append(quote)
        return quotesquotes = [quote for user in self.users.values() for quote in user.quotes if keyword in quote.text or keyword in quote.book.title or keyword in quote.book.author]quotes = [quote for user in self.users.values() for quote in user.quotes if keyword in quote.text or keyword in quote.book.title or keyword in quote.book.author]

    def add_quote(self, user, quote):
        user.quotes.append(quote)

    def view_book_progress(self, user):
        for book in user.bookshelf:
            if book.read:
                print(f"{book.title} by {book.author} - Read")
            else:
                print(f"{book.title} by {book.author} - {book.progress} pages read")for book in user.bookshelf:
            if book.read:
                print(f"{book.title} by {book.author} - Read")
            else:
                print(f"{book.title} by {book.author} - {book.progress} pages read")
            print('')
            print('Book Progress:')

    def update_book_progress(self, user, book, progress):
        for b in user.bookshelf:
            if b.title == book.title and b.author == book.author:
                b.update_progress(progress)
                print(f"Book progress updated: {book.title} by {book.author} - {progress} pages read")
                return
        print(f"Book not found: {book.title} by {book.author}")

# Main function
def main():
    bookverse = BookVerse()

    while True:
        print("\nBookVerse Menu:")
        print("1. Create User")
        print("2. Login User")
        print("3. Search Quotes")
        print("4. Add Quote")
        print("5. View Book Progress")
        print("6. Update Book Progress")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            bookverse.create_user(username)
        elif choice == "2":
            username = input("Enter username: ")
            user = bookverse.login_user(username)
            if user:
                while True:
                    print("\nUser Menu:")
                    print("1. View Bookshelf")
                    print("2. View Quotes")
                    print("3. Add Book")
                    print("4. Remove Book")
                    print("5. Logout")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        user.view_bookshelf()
                    elif choice == "2":
                        user.view_quotes()
                    elif choice == "3":
                        title = input("Enter book title: ")
                        author = input("Enter book author: ")
                        pages = int(input("Enter number of pages: "))
                        book = Book(title, author, pages)
                        user.add_book(book)
                    elif choice == "4":
                        title = input("Enter book title: ")
                        author = input("Enter book author: ")
                        for book in user.bookshelf:
                            if book.title == title and book.author == author:
                                user.remove_book(book)
                                print(f"Book removed: {title} by {author}")
                                break
                        else:
                            print(f"Book not found: {title} by {author}")
                    elif choice == "5":
                        break
        elif choice == "3":
            keyword = input("Enter search keyword: ")
            quotes = bookverse.search_quotes(keyword)
            for quote in quotes:
                print(f"{quote.text} - {quote.book.title} by {quote.book.author}")
        elif choice == "4":
            user = bookverse.login_user(input("Enter username: "))
            if user:
                text = input("Enter quote text: ")
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                book = Book(title, author, 0)
                quote = Quote(text, book)
                bookverse.add_quote(user, quote)
                quote.save_quote()
                quote.share_quote()
        elif choice == "5":
            user = bookverse.login_user(input("Enter username: "))
            if user:
                bookverse.view_book_progress(user)
        elif choice == "6":
            user = bookverse.login_user(input("Enter username: "))
            if user:
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                progress = int(input("Enter number of pages read: "))
                book = Book(title, author, 0)
                bookverse.update_book_progress(user, book, progress)
        elif choice == "7":
            break

if __name__ == "__main__":
    main()