-- Table Creation

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products Table
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Table
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE
);

-- Orders Table
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    shipping_address TEXT,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);

-- Order Items Table
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE
);

-- Reviews Table
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE
);

-- Sample Data Insertion

-- Users Insertion
INSERT INTO users (first_name, last_name, email, password_hash, phone, address)
VALUES
    ('John', 'Doe', 'john.doe@example.com', 'hashed_password_1', '555-1234', '123 Main St, Springfield, IL'),
    ('Jane', 'Smith', 'jane.smith@example.com', 'hashed_password_2', '555-5678', '456 Oak St, Springfield, IL');

-- Products Insertion
INSERT INTO products (name, description, price, category)
VALUES
    ('Laptop', 'High-performance laptop for gaming and productivity.', 1200.00, 'Electronics'),
    ('Smartphone', 'Latest model smartphone with a high-quality camera.', 800.00, 'Electronics'),
    ('Desk Chair', 'Ergonomic chair with adjustable height.', 150.00, 'Furniture'),
    ('Coffee Maker', 'Brew your favorite coffee with ease.', 75.00, 'Home Appliances');

-- Inventory Insertion
INSERT INTO inventory (product_id, quantity)
VALUES
    (1, 50),
    (2, 100),
    (3, 30),
    (4, 60);

-- Orders Insertion
INSERT INTO orders (user_id, total_amount, shipping_address)
VALUES
    (1, 1250.00, '123 Main St, Springfield, IL'),
    (2, 850.00, '456 Oak St, Springfield, IL');

-- Order Items Insertion
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
    (1, 1, 1, 1200.00),
    (1, 4, 1, 50.00),
    (2, 2, 1, 800.00);

-- Reviews Insertion
INSERT INTO reviews (user_id, product_id, rating, review_text)
VALUES
    (1, 1, 5, 'Excellent laptop for gaming! Highly recommend it.'),
    (2, 2, 4, 'Great smartphone, but a bit expensive. Still worth it.');

-- Sample Queries

-- 1. Retrieve all users
SELECT * FROM users;

-- 2. Retrieve all products with price greater than 100
SELECT * FROM products WHERE price > 100;

-- 3. Retrieve all products in the 'Electronics' category
SELECT * FROM products WHERE category = 'Electronics';

-- 4. Retrieve the current inventory for all products
SELECT p.name, i.quantity 
FROM inventory i 
JOIN products p ON i.product_id = p.product_id;

-- 5. Retrieve the total order amount for a specific user
SELECT o.order_id, o.total_amount, o.order_date
FROM orders o
WHERE o.user_id = 1;

-- 6. Get all items in an order
SELECT oi.order_item_id, p.name, oi.quantity, oi.price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE oi.order_id = 1;

-- 7. Update the inventory quantity for a product
UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 1;

-- 8. Add a new review for a product
INSERT INTO reviews (user_id, product_id, rating, review_text)
VALUES (2, 3, 3, 'The chair is comfortable, but the material feels cheap.');

-- 9. Retrieve the average rating for a product
SELECT p.name, AVG(r.rating) AS average_rating
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.product_id, p.name;  -- Add p.name in GROUP BY to avoid error

-- 10. Get all orders for a user, including the products ordered
SELECT o.order_id, p.name, oi.quantity, oi.price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.user_id = 1;

-- 11. Get the total sales amount for each product
SELECT p.name, SUM(oi.quantity * oi.price) AS total_sales
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name;  -- Add p.name in GROUP BY to avoid error

-- 12. Retrieve all products with reviews
SELECT p.name, r.rating, r.review_text
FROM reviews r
JOIN products p ON r.product_id = p.product_id
WHERE r.rating IS NOT NULL;

-- 13. Retrieve users who have placed an order
SELECT DISTINCT u.first_name, u.last_name, u.email
FROM users u
JOIN orders o ON u.user_id = o.user_id;

-- 14. Get the total number of products in inventory
SELECT SUM(quantity) AS total_inventory FROM inventory;

-- 15. Get the most expensive product in each category
SELECT category, name, MAX(price) AS highest_price
FROM products
GROUP BY category, name;  -- Add name in GROUP BY to avoid error

-- 16. Get all orders with their corresponding total and status
SELECT o.order_id, o.total_amount, o.status
FROM orders o
ORDER BY o.order_date DESC;

-- 17. Get the total amount spent by a user on all orders
SELECT u.first_name, u.last_name, SUM(o.total_amount) AS total_spent
FROM orders o
JOIN users u ON o.user_id = u.user_id
GROUP BY u.user_id, u.first_name, u.last_name;  -- Add first_name and last_name in GROUP BY

-- 18. Delete a product from the catalog and update inventory
DELETE FROM products WHERE product_id = 4;
UPDATE inventory SET quantity = 0 WHERE product_id = 4;

-- 19. Retrieve the number of reviews for each product
SELECT p.name, COUNT(r.review_id) AS review_count
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.name;  -- Add p.name in GROUP BY to avoid error

-- 20. Get orders that are 'Pending' and have a total amount greater than 1000
SELECT o.order_id, o.total_amount
FROM orders o
WHERE o.status = 'Pending' AND o.total_amount > 1000;
