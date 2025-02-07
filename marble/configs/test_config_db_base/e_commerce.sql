-- 1. Customers table (stores customer info)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,  -- Unique customer ID
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,  -- Unique email
    phone VARCHAR(20),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Products table (stores product details)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,  -- Unique product ID
    product_name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,  -- Product price
    stock_quantity INT NOT NULL,    -- Available stock
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Orders table (stores orders placed by customers)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,  -- Unique order ID
    customer_id INT REFERENCES customers(customer_id),  -- Foreign key to customers
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending'  -- Order status (e.g., pending, completed)
);

-- 4. Order_Items table (stores products in each order)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,  -- Unique order item ID
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,  -- Foreign key to orders
    product_id INT REFERENCES products(product_id),  -- Foreign key to products
    quantity INT NOT NULL,  -- Quantity of the product in the order
    price DECIMAL(10, 2) NOT NULL  -- Price of the product at the time of the order
);

-- 5. Payments table (stores payments for orders)
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,  -- Unique payment ID
    order_id INT REFERENCES orders(order_id) ON DELETE CASCADE,  -- Foreign key to orders
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2) NOT NULL,  -- Payment amount
    payment_method VARCHAR(50),  -- Payment method (e.g., credit card, PayPal)
    status VARCHAR(50) DEFAULT 'completed'  -- Payment status (e.g., completed, failed)
);

-- Insert customers
INSERT INTO customers (first_name, last_name, email, phone, address)
VALUES
('Alice', 'Smith', 'alice.smith@example.com', '123-456-7890', '123 Main St, Springfield'),
('Bob', 'Johnson', 'bob.johnson@example.com', '234-567-8901', '456 Oak St, Springfield');

-- Insert products
INSERT INTO products (product_name, description, price, stock_quantity)
VALUES
('Laptop', 'High-performance laptop', 999.99, 10),
('Smartphone', 'Latest model smartphone', 799.99, 15),
('Headphones', 'Noise-cancelling headphones', 199.99, 25);

-- Insert an order for Alice
INSERT INTO orders (customer_id, order_date, status)
VALUES
(1, '2024-12-13 10:00:00', 'pending');

-- Insert order items for Alice's order
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
(1, 1, 1, 999.99),  -- 1 Laptop
(1, 3, 2, 199.99);  -- 2 Headphones

-- Insert a payment for Alice's order
INSERT INTO payments (order_id, amount, payment_method, status)
VALUES
(1, 1399.97, 'Credit Card', 'completed');

-- Insert an order for Bob
INSERT INTO orders (customer_id, order_date, status)
VALUES
(2, '2024-12-13 12:00:00', 'pending');

-- Insert order items for Bob's order
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
(2, 2, 1, 799.99);  -- 1 Smartphone

-- Insert a payment for Bob's order
INSERT INTO payments (order_id, amount, payment_method, status)
VALUES
(2, 799.99, 'PayPal', 'completed');

SELECT oi.order_item_id, p.product_name, oi.quantity, oi.price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE oi.order_id = 1;  -- Get items for Alice's order (order_id = 1)

SELECT p.payment_id, p.payment_date, p.amount, p.payment_method, p.status
FROM payments p
WHERE p.order_id = 1;  -- Get payment details for Alice's order (order_id = 1)
