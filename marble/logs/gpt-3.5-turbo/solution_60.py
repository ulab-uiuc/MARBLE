# BookVerse - A platform for book enthusiasts

class QuoteDiscoveryModule:
    def __init__(self):
        self.quotes = []

    def search_by_title(self, title):
        # Search for quotes by book title
        return [quote for quote in self.quotes if title.lower() in quote['title'].lower()]

    def search_by_author(self, author):
        # Search for quotes by author
        return [quote for quote in self.quotes if author.lower() in quote['author'].lower()]

    def search_by_keyword(self, keyword):
        # Search for quotes by keyword
        return [quote for quote in self.quotes if keyword.lower() in quote['quote'].lower()]

    def save_favorite_quote(self, quote):
        # Save a quote as a favorite
        self.quotes.append(quote)

    def share_on_social_media(self, quote):
        # Share a quote on social media
        print(f"Shared: {quote}")


class ReadingProgressManagementModule:
    def __init__(self):
        self.bookshelf = {}

    def add_to_bookshelf(self, book, status='currently reading'):
        # Add a book to the virtual bookshelf
        self.bookshelf[book] = status

    def set_reading_goal(self, book, goal):
        # Set a reading goal for a book
        if book in self.bookshelf:
            self.bookshelf[book] = {'status': self.bookshelf[book], 'goal': goal}

    def update_progress(self, book, progress):
        # Update the reading progress (pages or chapters read)
        if book in self.bookshelf:
            if isinstance(self.bookshelf[book], str):
                self.bookshelf[book] = {'status': self.bookshelf[book], 'progress': progress}
            else:
                self.bookshelf[book]['progress'] = progress

    def mark_as_read(self, book):
        # Mark a book as 'read'
        if book in self.bookshelf:
            self.bookshelf[book] = 'read'


class BookReviewModule:
    def __init__(self):
        self.reviews = {}

    def write_review(self, book, review, rating):
        # Write a review and rate a book
        self.reviews[book] = {'review': review, 'rating': rating}

    def search_review(self, keyword):
        # Search for a review by keyword
        return {book: review for book, review in self.reviews.items() if keyword.lower() in review['review'].lower()}

    def filter_review_by_rating(self, min_rating):        if book in self.reviews:
            self.reviews[book]['review'] = new_review
            self.reviews[book]['rating'] = new_rating        if book in self.reviews:
            self.reviews[book]['review'] = new_review
            self.reviews[book]['rating'] = new_rating
        # Filter reviews by minimum rating
        return {book: review for book, review in self.reviews.items() if review['rating'] >= min_rating}


# Example Usage
quote_module = QuoteDiscoveryModule()
quote_module.save_favorite_quote({'title': 'Book1', 'author': 'Author1', 'quote': 'Quote1'})
quote_module.save_favorite_quote({'title': 'Book2', 'author': 'Author2', 'quote': 'Quote2'})
print(quote_module.search_by_title('Book1'))

progress_module = ReadingProgressManagementModule()
progress_module.add_to_bookshelf('Book1')
progress_module.set_reading_goal('Book1', 100)
progress_module.update_progress('Book1', 50)
progress_module.mark_as_read('Book1')

review_module = BookReviewModule()
review_module.write_review('Book1', 'Great book!', 5)
print(review_module.search_review('Great'))
print(review_module.filter_review_by_rating(4))