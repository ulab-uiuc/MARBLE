# solution.py

# BookVerse Application

class Quote:
    """Class to represent a quote from a book."""
    def __init__(self, text, author, book_title):
        self.text = text
        self.author = author
        self.book_title = book_title

class QuoteDiscovery:
    """Module for discovering and managing quotes."""
    def __init__(self):
        self.quotes = []  # List to store quotes
        self.favorite_quotes = []  # List to store favorite quotes

    def add_quote(self, quote):
        """Add a new quote to the collection."""
        self.quotes.append(quote)

    def search_quotes(self, search_term):
        """Search for quotes by book title, author, or keyword."""
        results = [quote for quote in self.quotes if 
                   search_term.lower() in quote.text.lower() or 
                   search_term.lower() in quote.author.lower() or 
                   search_term.lower() in quote.book_title.lower()]
        return results

    def save_favorite(self, quote):
        """Save a quote as a favorite."""
        if quote not in self.favorite_quotes:
            self.favorite_quotes.append(quote)

    def share_quote(self, quote):
        """Simulate sharing a quote on social media."""
        return f"Sharing quote: '{quote.text}' by {quote.author} from '{quote.book_title}'"

class UserProfile:
    """Class to manage user profiles."""
    def __init__(self, username):
        self.username = username
        self.bookshelf = []  # List to store books
        self.reading_progress = {}  # Dictionary to track reading progress

    def add_book(self, book_title):
        """Add a book to the user's bookshelf."""
        self.bookshelf.append(book_title)
        self.reading_progress[book_title] = {'status': 'currently reading', 'pages_read': 0}

    def mark_as_read(self, book_title):
        if book_title in self.reading_progress:
            self.reading_progress[book_title]['status'] = 'read'
    def set_reading_goal(self, book_title, goal):
        """Set a reading goal for a book."""
        if book_title in self.reading_progress:
            self.reading_progress[book_title]['goal'] = goal
        else:
            raise ValueError('Book not found in reading progress.')

    def update_reading_goal(self, book_title, new_goal):
        """Update the reading goal for a book."""
        if book_title in self.reading_progress:
            self.reading_progress[book_title]['goal'] = new_goal
        else:
            raise ValueError('Book not found in reading progress.')        if book_title in self.reading_progress:
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
        results = {title: review for title, review in self.reviews.items() if search_term.lower() in title.lower()}
        return results

# Example usage
if __name__ == "__main__":
    # Initialize modules
    quote_discovery = QuoteDiscovery()
    user_profile = UserProfile("book_lover")
    book_review = BookReview()

    # Add quotes
    quote1 = Quote("To be, or not to be, that is the question.", "William Shakespeare", "Hamlet")
    quote2 = Quote("The only thing we have to fear is fear itself.", "Franklin D. Roosevelt", "Inaugural Address")
    quote_discovery.add_quote(quote1)
    quote_discovery.add_quote(quote2)

    # Search for quotes
    found_quotes = quote_discovery.search_quotes("fear")
    for quote in found_quotes:
        print(f"Found Quote: '{quote.text}' by {quote.author} from '{quote.book_title}'")

    # Save a favorite quote
    quote_discovery.save_favorite(quote1)

    # Add a book to the user's profile
    user_profile.add_book("Hamlet")
    user_profile.update_progress("Hamlet", 50)  # Update progress after reading 50 pages
    user_profile.mark_as_read("Hamlet")  # Mark as read

    # Add a review for a book
    book_review.add_review("Hamlet", "A profound exploration of the human condition.", 5)

    # Retrieve and print the review
    review = book_review.get_review("Hamlet")
    print(f"Review for Hamlet: {review['review']} (Rating: {review['rating']})")