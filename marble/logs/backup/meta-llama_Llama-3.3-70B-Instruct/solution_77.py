# solution.py
import sqlite3
from sqlite3 import Error
import threading
import time
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

# Database class to handle database operations
class Database:    def create_tables(self):
class User(self.Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
class Group(self.Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
class UserGroup(self.Base):
    __tablename__ = 'user_groups'
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
class Product(self.Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
class Watchlist(self.Base):
    __tablename__ = 'watchlist'
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    price_threshold = Column(Float)
    def register_user(self, email, password):
        user = User(email=email, password=password)
        self.session.add(user)
        self.session.commit()
    def login_user(self, email, password):
        user = self.session.query(User).filter_by(email=email, password=password).first()
        return user
    def create_group(self, name):
        group = Group(name=name)
        self.session.add(group)
        self.session.commit()
    def join_group(self, user_id, group_id):
        user_group = UserGroup(user_id=user_id, group_id=group_id)
        self.session.add(user_group)
        self.session.commit()
    def add_product(self, url, name):
        product = Product(url=url, name=name)
        self.session.add(product)
        self.session.commit()
    def add_to_watchlist(self, user_id, product_id, price_threshold):
        watchlist = Watchlist(user_id=user_id, product_id=product_id, price_threshold=price_threshold)
        self.session.add(watchlist)
        self.session.commit()
        self.Base.metadata.create_all(self.engine)with threading.Lock():
        # Create users table
        users_table = """CREATE TABLE IF NOT EXISTS users (users_table = """CREATE TABLE IF NOT EXISTS users (
                            id integer PRIMARY KEY,
                            email text NOT NULL,
                            password text NOT NULL
                        );"""
        try:
            c = self.conn.cursor()
            c.execute(users_table)
        except Error as e:
            print(e)

        # Create groups table
from sqlalchemy import inspect
with self.engine.connect() as conn:
    inspector = inspect(conn)
    if 'users' not in inspector.get_table_names():
        # Create users table
        groups_table =groups_table = """CREATE TABLE IF NOT EXISTS groups (
                            id integer PRIMARY KEY,
                            name text NOT NULL
                        );"""try:
            c = self.conn.cursor()
            c.execute(groups_table)
        except Error as e:
            print(e)

        # Create user_groups table
        user_groups_table =user_groups_table = """CREATE TABLE IF NOT EXISTS user_groups (
                                user_id integer NOT NULL,
                                group_id integer NOT NULL,
                                PRIMARY KEY (user_id, group_id),
                                FOREIGN KEY (user_id) REFERENCES users (id),
                                FOREIGN KEY (group_id) REFERENCES groups (id)
                            );"""try:
            c = self.conn.cursor()
            c.execute(user_groups_table)
        except Error as e:
            print(e)

        # Create products table
        products_table =products_table = """CREATE TABLE IF NOT EXISTS products (
                            id integer PRIMARY KEY,
                            url text NOT NULL,
                            name text NOT NULL
                        );"""try:
            c = self.conn.cursor()
            c.execute(products_table)
        except Error as e:
            print(e)

        # Create watchlist table
        watchlist_table =watchlist_table = """CREATE TABLE IF NOT EXISTS watchlist (
                            user_id integer NOT NULL,
                            product_id integer NOT NULL,
                            price_threshold real NOT NULL,
                            PRIMARY KEY (user_id, product_id),
                            FOREIGN KEY (user_id) REFERENCES users (id),
                            FOREIGN KEY (product_id) REFERENCES products (id)
                        );"""try:
            c = self.conn.cursor()
            c.execute(watchlist_table)
        except Error as e:
            print(e)

        # Create notifications tabledef get_price(self, url):
        try:
            response = requests.get(url)price_element = soup.find('span', {'class': 'price'}) or soup.find('span', {'class': 'price-tag'}) or soup.find('p', {'class': 'price'})
        if price_element:
            price = price_element.text.strip()            return float(price)
            else:
                raise ValueError('Price not found')
        except Exception as e:
            print(e)
            return None            return float(price)
        except Exception as e:
            print(e)
            return None

    def check_price(self, user_id, product_id):
        try:
            c = self.conn.cursor()
            c.execute("SELECT price_threshold FROM watchlist WHERE user_id = ? AND product_id = ?", (user_id, product_id))
            price_threshold = c.fetchone()[0]
            price = self.get_price(self.get_url(product_id))
            if price and price < price_threshold:
                self.send_notification(user_id, product_id, f"Price dropped to {price}")
                return True
                self.conn.execute("COMMIT")
            return False
                self.conn.execute("ROLLBACK")
        except Error as e:
            print(e)
            return False

    def get_url(self, product_id):
        try:
        with threading.Lock():
            try:
                self.conn.execute("BEGIN TRANSACTION")
            c = self.conn.cursor()
            c.execute("SELECT url FROM products WHERE id = ?", (product_id,))
            return c.fetchone()[0]
        except Error as e:
            print(e)
            return None

    def send_notification(self, user_id, product_id, message):
        try:with self.engine.connect() as conn:
    conn.execute(text("INSERT INTO notifications (user_id, product_id, message) VALUES (:user_id, :product_id, :message)"), user_id=user_id, product_id=product_id, message=message)
            self.send_email(user_id, message)
            return True
        except Error as e:
            print(e)
            return False

    def send_email(self, user_id, message):
        try:
            c = self.conn.cursor()
            c.execute("SELECT email FROM users WHERE id = ?", (user_id,))
            email = c.fetchone()[0]
            msg = MIMEMultipart()
            msg['From'] = 'your-email@gmail.com'
            msg['To'] = email
            msg['Subject'] = 'Price Alert'
            body = message
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(msg['From'], 'your-password')
            text = msg.as_string()
            server.sendmail(msg['From'], msg['To'], text)
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False

# PriceTrackerCollaborator class
class PriceTrackerCollaborator:
    def __init__(self, db_file):
        self.db = Database(db_file)
        self.db.create_tables()

    def register(self, email, password):
        return self.db.register_user(email, password)

    def login(self, email, password):
        return self.db.login_user(email, password)

    def create_group(self, name):
        return self.db.create_group(name)

    def join_group(self, user_id, group_id):
        return self.db.join_group(user_id, group_id)

    def add_product(self, url, name):
        return self.db.add_product(url, name)

    def add_to_watchlist(self, user_id, product_id, price_threshold):
        return self.db.add_to_watchlist(user_id, product_id, price_threshold)

    def check_price(self, user_id, product_id):
        return self.db.check_price(user_id, product_id)

    def start(self):
        while True:
            # Check prices for all users
            c = self.db.conn.cursor()
            c.execute("SELECT user_id, product_id FROM watchlist")
            watchlist = c.fetchall()
            for user_id, product_id in watchlist:
                self.check_price(user_id, product_id)
            time.sleep(60)  # Check prices every minute

# Test the application
if __name__ == '__main__':
    app = PriceTrackerCollaborator('price_tracker.db')
    app.register('user1@example.com', 'password1')
    app.register('user2@example.com', 'password2')
    app.create_group('Group1')
    app.join_group(1, 1)
    app.join_group(2, 1)
    app.add_product('https://example.com/product1', 'Product1')
    app.add_to_watchlist(1, 1, 100.0)
    app.add_to_watchlist(2, 1, 90.0)
    threading.Thread(target=app.start).start()

# test.py
import unittest
from solution import PriceTrackerCollaborator

class TestPriceTrackerCollaborator(unittest.TestCase):
    def setUp(self):
        self.app = PriceTrackerCollaborator('test.db')

    def test_register(self):
        self.assertTrue(self.app.register('user1@example.com', 'password1'))

    def test_login(self):
        self.app.register('user1@example.com', 'password1')
        self.assertTrue(self.app.login('user1@example.com', 'password1'))

    def test_create_group(self):
        self.assertTrue(self.app.create_group('Group1'))

    def test_join_group(self):
        self.app.create_group('Group1')
        self.app.register('user1@example.com', 'password1')
        self.assertTrue(self.app.join_group(1, 1))

    def test_add_product(self):
        self.assertTrue(self.app.add_product('https://example.com/product1', 'Product1'))

    def test_add_to_watchlist(self):
        self.app.add_product('https://example.com/product1', 'Product1')
        self.app.register('user1@example.com', 'password1')
        self.assertTrue(self.app.add_to_watchlist(1, 1, 100.0))

    def test_check_price(self):
        self.app.add_product('https://example.com/product1', 'Product1')
        self.app.register('user1@example.com', 'password1')
        self.app.add_to_watchlist(1, 1, 100.0)
        self.assertTrue(self.app.check_price(1, 1))

if __name__ == '__main__':
    unittest.main()