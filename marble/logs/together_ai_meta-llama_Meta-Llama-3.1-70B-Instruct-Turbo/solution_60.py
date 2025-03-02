
# book_repository.py

class BookRepository:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def get_books(self):
        return self.books# bookverse.py

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.quotes = []
        self.reviews = []
        self.reading_progress = 0

    def add_quote(self, quote):
        self.quotes.append(quote)

    def add_review(self, review):
        self.reviews.append(review)

    def update_reading_progress(self, progress):
        self.reading_progress = progress


class User:
    def __init__(self, name):
        self.name = name
        self.bookshelf = []
        self.favorite_quotes = []

    def add_book_to_bookshelf(self, book):
        self.bookshelf.append(book)

    def add_favorite_quote(self, quote):
        self.favorite_quotes.append(quote)


class QuoteDiscoveryModule:
    def __init__(self):
        self.book_repository = BookRepository()
        self.books.append(book)

    def search_quotes_by_title(self, title):
        for book in self.books:for book in self.book_repository.get_books():
            if book.title.lower() == title.lower():
                return book.quotes
        return []

    def search_quotes_by_author(self, author):
        quotes = []
        for book in self.books:for book in self.book_repository.get_books():
            if book.author.lower() == author.lower():
                quotes.extend(book.quotes)
        return quotes

    def search_quotes_by_keyword(self, keyword):
        quotes = []
        for book in self.books:for book in self.book_repository.get_books():
            for quote in book.quotes:
                if keyword.lower() in quote.lower():
                    quotes.append(quote)
        return quotes


class ReadingProgressManagementModule:
    def __init__(self):
        self.book_repository = BookRepository()
        self.users.append(user)

    def update_reading_progress(self, user, book, progress):
        for user_book in user.bookshelf:
            if user_book.title == book.title:
                user_book.update_reading_progress(progress)
                break


class BookReviewModule:
    def __init__(self):
        self.book_repository = BookRepository()
        self.books.append(book)

    def add_review(self, book, review):
        for b in self.books:
            if b.title == book.title:
                b.add_review(review)
                break

    def search_reviews_by_title(self, title):
        for book in self.books:for book in self.book_repository.get_books():
            if book.title.lower() == title.lower():
                return book.reviews
        return []

    def search_reviews_by_author(self, author):
        reviews = []
        for book in self.books:for book in self.book_repository.get_books():
            if book.author.lower() == author.lower():
                reviews.extend(book.reviews)
        return reviews


class BookVerse:
    def __init__(self):
        self.quote_discovery_module = QuoteDiscoveryModule()
        self.reading_progress_management_module = ReadingProgressManagementModule()
        self.book_review_module = BookReviewModule()

    def run(self):
        # Create books
        book1 = Book("Book1", "Author1")
        book1.add_quote("Quote1")
        book1.add_quote("Quote2")

        book2 = Book("Book2", "Author2")
        book2.add_quote("Quote3")
        book2.add_quote("Quote4")

        # Add books to quote discovery module
        self.book_repository.add_book(book1)
        self.quote_discovery_module.add_book(book2)

        # Create user
        user = User("User1")

        # Add books to user's bookshelf
        user.add_book_to_bookshelf(book1)
        user.add_book_to_bookshelf(book2)

        # Add user to reading progress management module
        self.reading_progress_management_module.add_user(user)

        # Update reading progress
        self.reading_progress_management_module.update_reading_progress(user, book1, 50)

        # Add reviews to book review module
        self.book_review_module.add_book(book1)self.book_repository.add_book(book1)
        self.book_review_module.add_book(book2)
        self.book_review_module.add_review(book1, "Review1")
        self.book_review_module.add_review(book2, "Review2")

        # Search quotes
        print("Search quotes by title:")
        print(self.quote_discovery_module.search_quotes_by_title("Book1"))

        print("Search quotes by author:")
        print(self.quote_discovery_module.search_quotes_by_author("Author1"))

        print("Search quotes by keyword:")
        print(self.quote_discovery_module.search_quotes_by_keyword("Quote"))

        # Search reviews
        print("Search reviews by title:")
        print(self.book_review_module.search_reviews_by_title("Book1"))

        print("Search reviews by author:")
        print(self.book_review_module.search_reviews_by_author("Author1"))


if __name__ == "__main__":
    bookverse = BookVerse()
    bookverse.run()