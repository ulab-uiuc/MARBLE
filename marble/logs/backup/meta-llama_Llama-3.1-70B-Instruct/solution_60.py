# bookverse.py

class Book:
    """Represents a book with title, author, and quotes."""
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.quotes = []

    def add_quote(self, quote):
        """Adds a quote to the book."""
        self.quotes.append(quote)

    def __str__(self):
        return f"{self.title} by {self.author}"


class User:
    """Represents a user with a profile and bookshelf."""
    def __init__(self, name):
        self.name = name
        self.bookshelf = []
        self.reading_goals = {}

    def add_book(self, book):
        """Adds a book to the user's bookshelf."""
        self.bookshelf.append(book)

    def set_reading_goal(self, book, goal):
        """Sets a reading goal for a book."""
        self.reading_goals[book] = goal

    def __str__(self):
        return f"{self.name}'s Profile"


class QuoteDiscoveryModule:
    """Provides functionalities for quote discovery."""
    def __init__(self):
        self.books = []

    def add_book(self, book):
        """Adds a book to the quote discovery module."""
        self.books.append(book)

    def search_by_title(self, title):
        """Searches for books by title."""
        return [book for book in self.books if book.title.lower() == title.lower()]

    def search_by_author(self, author):
        """Searches for books by author."""
        return [book for book in self.books if book.author.lower() == author.lower()]

    def search_by_keyword(self, keyword):
        """Searches for books by keyword."""
        return [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower()]

    def save_quote(self, book, quote):
        """Saves a quote from a book."""
        book.add_quote(quote)

    def share_quote(self, book, quote):
        """Shares a quote from a book on social media."""
        print(f"Sharing '{quote}' from {book} on social media...")


class ReadingProgressManagementModule:
    """Provides functionalities for reading progress management."""
    def __init__(self):
        self.users = []

    def add_user(self, user):
        """Adds a user to the reading progress management module."""
        self.users.append(user)

    def add_book_to_bookshelf(self, user, book):
        """Adds a book to a user's bookshelf."""
        user.add_book(book)

    def set_reading_goal(self, user, book, goal):
        """Sets a reading goal for a book."""
        user.set_reading_goal(book, goal)

    def mark_as_read(self, user, book):
        """Marks a book as read."""
        print(f"{book} marked as read by {user}")


class BookReviewModule:def add_review(self, user, book, review, rating):self.reviews.append((user, book, review))

    def search_reviews(self, book):
        """Searches for reviews of a book."""
        return [review for review in self.reviews if review[1] == book]

    def filter_reviews(self, rating):return [review for review in self.reviews if review[3] >= rating]
        """Filters reviews by rating."""
        return [review for review in self.reviews if review[2] >= rating]


class BookVerse:
    """The main application class."""
    def __init__(self):
        self.quote_discovery_module = QuoteDiscoveryModule()
        self.reading_progress_management_module = ReadingProgressManagementModule()
        self.book_review_module = BookReviewModule()

    def run(self):
        # Create a book
        book = Book("To Kill a Mockingbird", "Harper Lee")

        # Create a user
        user = User("John Doe")

        # Add the book to the quote discovery module
        self.quote_discovery_module.add_book(book)

        # Add the user to the reading progress management module
        self.reading_progress_management_module.add_user(user)

        # Add the book to the user's bookshelf
        self.reading_progress_management_module.add_book_to_bookshelf(user, book)

        # Set a reading goal for the book
        self.reading_progress_management_module.set_reading_goal(user, book, 500)

        # Search for quotes by title
        results = self.quote_discovery_module.search_by_title("To Kill a Mockingbird")
        print("Search results:")
        for result in results:
            print(result)

        # Save a quote from the book
        self.quote_discovery_module.save_quote(book, "You never really understand a person until you consider things from his point of view...")

        # Share the quote on social media
        self.quote_discovery_module.share_quote(book, "You never really understand a person until you consider things from his point of view...")

        # Mark the book as read
        self.reading_progress_management_module.mark_as_read(user, book)

        # Add a review for the book
        self.book_review_module.add_review(user, book, 5)

        # Search for reviews of the book
        reviews = self.book_review_module.search_reviews(book)
        print("Reviews:")
        for review in reviews:
            print(review)


if __name__ == "__main__":
    bookverse = BookVerse()
    bookverse.run()