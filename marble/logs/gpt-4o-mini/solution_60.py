# solution.py

# BookVerse Application

class Quote:
    """Class to represent a quote from a book."""
    def __init__(self, text, author, book_title):
        self.text = text  # The text of the quote
        self.author = author  # The author of the quote
        self.book_title = book_title  # The title of the book from which the quote is taken

class QuoteDiscovery:
    """Module for discovering and managing quotes."""
    def __init__(self):
        self.quotes = []  # List to store quotes
        self.favorite_quotes = []  # List to store favorite quotes

    def add_quote(self, quote):
        """Add a new quote to the collection."""
        self.quotes.append(quote)def search_quotes(self, search_terms):
        """Search for quotes by book title, author, or multiple keywords."""
        search_terms = search_terms.lower().split()  # Split the input into individual keywords
        return [quote for quote in self.quotes if any(term in quote.book_title.lower() or
                                                       term in quote.author.lower() or
                                                       term in quote.text.lower() for term in search_terms)]    def save_favorite(self, quote):
        """Save a quote as a favorite."""
        if quote not in self.favorite_quotes:
            self.favorite_quotes.append(quote)

    def share_quote(self, quote):
        """Simulate sharing a quote on social media."""
        return f"Sharing quote: '{quote.text}' by {quote.author} from '{quote.book_title}'"

class UserProfile:
    """Class to manage user profiles."""
    def __init__(self, username):
        self.username = username  # The username of the user
        self.bookshelf = []  # List to store books in the user's bookshelf
        self.reading_progress = {}  # Dictionary to track reading progress

    def add_book(self, book_title):
        """Add a book to the user's bookshelf."""
        self.bookshelf.append(book_title)
        self.reading_progress[book_title] = {'status': 'currently reading', 'pages_read': 0}

    def mark_as_read(self, book_title):
        """Mark a book as read."""
        if book_title in self.reading_progress:
            self.reading_progress[book_title]['status'] = 'read'

    def update_progress(self, book_title, pages):
        """Update the reading progress for a book."""
        if book_title in self.reading_progress:
            self.reading_progress[book_title]['pages_read'] += pages

class BookReview:
    """Class to manage book reviews."""
    def __init__(self):
        self.reviews = {}  # Dictionary to store reviews by book title

    def add_review(self, book_title, review_text, rating):
        """Add a review for a book."""
        self.reviews[book_title] = {'review': review_text, 'rating': rating}

    def get_review(self, book_title):
        """Get the review for a specific book."""
        return self.reviews.get(book_title, "No review found.")

    def search_reviews(self, search_term):
        """Search for reviews by book title."""
        return {title: review for title, review in self.reviews.items() if search_term.lower() in title.lower()}

# Example usage
if __name__ == "__main__":
    # Create instances of the modules
    quote_discovery = QuoteDiscovery()
    user_profile = UserProfile("book_lover")
    book_review = BookReview()

    # Adding quotes
    quote1 = Quote("To be, or not to be, that is the question.", "William Shakespeare", "Hamlet")
    quote2 = Quote("The only thing we have to fear is fear itself.", "Franklin D. Roosevelt", "Inaugural Address")
    quote_discovery.add_quote(quote1)
    quote_discovery.add_quote(quote2)

    # Searching for quotes
    found_quotes = quote_discovery.search_quotes("fear")
    for quote in found_quotes:
        print(f"Found Quote: '{quote.text}' by {quote.author} from '{quote.book_title}'")

    # Saving a favorite quote
    quote_discovery.save_favorite(quote1)

    # User profile actions
    user_profile.add_book("Hamlet")
    user_profile.update_progress("Hamlet", 50)
    user_profile.mark_as_read("Hamlet")

    # Adding a review
    book_review.add_review("Hamlet", "A profound exploration of the human condition.", 5)

    # Retrieving a review
    print(book_review.get_review("Hamlet"))