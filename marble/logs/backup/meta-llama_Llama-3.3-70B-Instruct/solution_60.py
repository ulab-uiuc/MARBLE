# solution.py

# Importing necessary libraries
import sqlite3
from sqlite3 import Error

# Quote Discovery Module
class QuoteDiscoveryModule:def __init__(self, db_name, user_id):
        self.db_name = db_name
        self.user_id = user_id
        self.conn = None        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connected to {self.db_name} database.")
        except Error as e:
            print(e)

    def create_quote_table(self):
        """
        Create a table for quotes in the database.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY,
                book_title TEXT,
                author TEXT,
                keyword TEXT,
                quote TEXT
            );
        """
        try:
            self.conn.execute(create_table_query)
            print("Quote table created.")
        except Error as e:
            print(e)

    def search_quote_by_book_title(self, book_title):
        """
        Search for quotes by book title.
        
        Args:
        book_title (str): The title of the book.
        
        Returns:
        list: A list of quotes matching the book title.
        """
        search_query = """
            SELECT quote FROM quotes
            WHERE book_title = ?;
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(search_query, (book_title,))
            quotes = cursor.fetchall()
            return quotes
        except Error as e:
            print(e)

    def search_quote_by_author(self, author):
        """
        Search for quotes by author.
        
        Args:
        author (str): The author of the book.
        
        Returns:
        list: A list of quotes matching the author.
        """
        search_query = """
            SELECT quote FROM quotes
            WHERE author = ?;
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(search_query, (author,))
            quotes = cursor.fetchall()
            return quotes
        except Error as e:
            print(e)

    def search_quote_by_keyword(self, keyword):
        """
        Search for quotes by keyword.
        
        Args:
        keyword (str): The keyword to search for.
        
        Returns:
        list: A list of quotes matching the keyword.
        """
        search_query = """
            SELECT quote FROM quotes
            WHERE keyword = ?;
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(search_query, (keyword,))
            quotes = cursor.fetchall()
            return quotes
        except Error as e:
            print(e)

    def save_favorite_quote(self, quote):
        """
        Save a favorite quote.
        
        Args:
        quote (str): The quote to save.
        """
        save_query = """
            INSERT INTO quotes (quote)
            VALUES (?);
        """
        try:
            self.conn.execute(save_query, (quote,))
            self.conn.commit()
            print("Quote saved.")
        except Error as e:
            print(e)

    def share_quote_on_social_media(self, quote):
        """
        Share a quote on social media.
        
        Args:
        quote (str): The quote to share.
        """
        # This function can be implemented using social media APIs
        print("Quote shared on social media.")


# Reading Progress Management Module
class ReadingProgressManagementModule:
    def __init__(self, db_name):
        """
        Initialize the Reading Progress Management Module with a database name.
        
        Args:
        db_name (str): The name of the database.
        """
        self.db_name = db_name
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connected to {self.db_name} database.")
        except Error as e:
            print(e)

    def create_bookshelf_table(self):
        """
        Create a table for the bookshelf in the database.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS bookshelf (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                book_title TEXT,
                author TEXT,
                pages_read INTEGER,
                chapters_read INTEGER,
                status TEXT
            );
        """
        try:
            self.conn.execute(create_table_query)
            print("Bookshelf table created.")
        except Error as e:
            print(e)

    def add_book_to_bookshelf(self, user_id, book_title, author):
        """
        Add a book to the bookshelf.
        
        Args:
        user_id (int): The ID of the user.
        book_title (str): The title of the book.
        author (str): The author of the book.
        """
        add_book_query = """
            INSERT INTO bookshelf (user_id, book_title, author, pages_read, chapters_read, status)
            VALUES (?, ?, ?, 0, 0, 'currently reading');
        """
        try:
            self.conn.execute(add_book_query, (user_id, book_title, author))
            self.conn.commit()
            print("Book added to bookshelf.")
        except Error as e:
            print(e)

    def set_reading_goal(self, user_id, book_title, pages_to_read):
        """
        Set a reading goal for a book.
        
        Args:
        user_id (int): The ID of the user.
        book_title (str): The title of the book.
        pages_to_read (int): The number of pages to read.
        """
        set_goal_query = """
            UPDATE bookshelf
            SET pages_read = ?
            WHERE user_id = ? AND book_title = ?;
        """
        try:
            self.conn.execute(set_goal_query, (pages_to_read, user_id, book_title))
            self.conn.commit()
            print("Reading goal set.")
        except Error as e:
            print(e)

    def track_reading_progress(self, user_id, book_title, pages_read, chapters_read):
        """
        Track the reading progress of a book.
        
        Args:
        user_id (int): The ID of the user.
        book_title (str): The title of the book.
        pages_read (int): The number of pages read.
        chapters_read (int): The number of chapters read.
        """
        track_progress_query = """
            UPDATE bookshelf
            SET pages_read = ?, chapters_read = ?
            WHERE user_id = ? AND book_title = ?;
        """
        try:
            self.conn.execute(track_progress_query, (pages_read, chapters_read, user_id, book_title))
            self.conn.commit()
            print("Reading progress tracked.")
        except Error as e:
            print(e)

    def mark_book_as_read(self, user_id, book_title):
        """
        Mark a book as read.
        
        Args:
        user_id (int): The ID of the user.
        book_title (str): The title of the book.
        """
        mark_as_read_query = """
            UPDATE bookshelf
            SET status = 'read'
            WHERE user_id = ? AND book_title = ?;
        """
        try:
            self.conn.execute(mark_as_read_query, (user_id, book_title))
            self.conn.commit()
            print("Book marked as read.")
        except Error as e:
            print(e)


# Book Review Module
class BookReviewModule:
    def __init__(self, db_name):
        """
        Initialize the Book Review Module with a database name.
        
        Args:
        db_name (str): The name of the database.
        """
        self.db_name = db_name
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connected to {self.db_name} database.")
        except Error as e:
            print(e)

    def create_review_table(self):
        """
        Create a table for reviews in the database.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                book_title TEXT,
                author TEXT,
                review TEXT,
                rating INTEGER
            );
        """
        try:
            self.conn.execute(create_table_query)
            print("Review table created.")
        except Error as e:
            print(e)

    def write_review(self, user_id, book_title, author, review, rating):
        """
        Write a review for a book.
        
        Args:
        user_id (int): The ID of the user.
        book_title (str): The title of the book.
        author (str): The author of the book.
        review (str): The review of the book.
        rating (int): The rating of the book.
        """
        write_review_query = """
            INSERT INTO reviews (user_id, book_title, author, review, rating)
            VALUES (?, ?, ?, ?, ?);
        """
        try:
            self.conn.execute(write_review_query, (user_id, book_title, author, review, rating))
            self.conn.commit()
            print("Review written.")
        except Error as e:
            print(e)

    def search_review_by_book_title(self, book_title):
        """
        Search for reviews by book title.
        
        Args:
        book_title (str): The title of the book.
        
        Returns:
        list: A list of reviews matching the book title.
        """
        search_query = """
            SELECT review FROM reviews
            WHERE book_title = ?;
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(search_query, (book_title,))
            reviews = cursor.fetchall()
            return reviews
        except Error as e:
            print(e)

    def search_review_by_author(self, author):
        """
        Search for reviews by author.
        
        Args:
        author (str): The author of the book.
        
        Returns:
        list: A list of reviews matching the author.
        """
        search_query = """
            SELECT review FROM reviews
            WHERE author = ?;
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(search_query, (author,))
            reviews = cursor.fetchall()
            return reviews
        except Error as e:
            print(e)

    def update_review(self, user_id, book_title, review, rating):
        """
        Update a review for a book.
        
        Args:
        user_id (int): The ID of the user.
        book_title (str): The title of the book.
        review (str): The updated review of the book.
        rating (int): The updated rating of the book.
        """
        update_query = """
            UPDATE reviews
            SET review = ?, rating = ?
            WHERE user_id = ? AND book_title = ?;
        """
        try:
            self.conn.execute(update_query, (review, rating, user_id, book_title))
            self.conn.commit()
            print("Review updated.")
        except Error as e:
            print(e)


# Main function
def main():
    db_name = "bookverse.db"
    
    # Create instances of the modules
    quote_discovery_module = QuoteDiscoveryModule(db_name)
    reading_progress_management_module = ReadingProgressManagementModule(db_name)
    book_review_module = BookReviewModule(db_name)
    
    # Create tables
    quote_discovery_module.create_quote_table()
    reading_progress_management_module.create_bookshelf_table()
    book_review_module.create_review_table()
    
    # Test the modules
    quote_discovery_module.save_favorite_quote("This is a favorite quote.")
    quote_discovery_module.share_quote_on_social_media("This is a quote to share.")
    
    reading_progress_management_module.add_book_to_bookshelf(1, "Book Title", "Author")
    reading_progress_management_module.set_reading_goal(1, "Book Title", 100)
    reading_progress_management_module.track_reading_progress(1, "Book Title", 50, 2)
    reading_progress_management_module.mark_book_as_read(1, "Book Title")
    
    book_review_module.write_review(1, "Book Title", "Author", "This is a review.", 5)
    book_review_module.search_review_by_book_title("Book Title")
    book_review_module.search_review_by_author("Author")
    book_review_module.update_review(1, "Book Title", "This is an updated review.", 4)


if __name__ == "__main__":
    main()