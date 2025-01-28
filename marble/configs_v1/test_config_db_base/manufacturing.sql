-- 1. Customers table (stores information about customers)
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,  -- Unique customer ID
    company_name VARCHAR(255) NOT NULL,  -- Customer company name
    contact_name VARCHAR(100),  -- Customer contact person
    contact_email VARCHAR(255) UNIQUE NOT NULL,  -- Customer contact email
    phone VARCHAR(20),  -- Customer contact phone number
    address VARCHAR(255),  -- Customer address
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Customer registration time
);

-- 2. Products table (stores details of products)
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,  -- Unique product ID
    product_name VARCHAR(255) NOT NULL,  -- Product name
    description TEXT,  -- Product description
    price DECIMAL(10, 2) NOT NULL,  -- Product price
    category VARCHAR(100),  -- Product category (e.g., electronics, machinery)
    stock_quantity INT NOT NULL,  -- Available stock quantity
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Product creation time
);

-- 3. Suppliers table (stores information about suppliers)
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,  -- Unique supplier ID
    company_name VARCHAR(255) NOT NULL,  -- Supplier company name
    contact_name VARCHAR(100),  -- Supplier contact person
    contact_email VARCHAR(255) UNIQUE NOT NULL,  -- Supplier contact email
    phone VARCHAR(20),  -- Supplier contact phone number
    address VARCHAR(255),  -- Supplier address
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Supplier registration time
);

-- 4. Orders table (stores orders made by customers)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,  -- Unique order ID
    customer_id INT REFERENCES customers(customer_id),  -- Foreign key to customers
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of order
    status VARCHAR(50) DEFAULT 'pending',  -- Order status (e.g., pending, completed)
    total_amount DECIMAL(10, 2)  -- Total amount of the order
);

-- 5. Order_Items table (stores details of items in each order)
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,  -- Unique order item ID
    order_id INT REFERENCES orders(order_id),  -- Foreign key to orders
    product_id INT REFERENCES products(product_id),  -- Foreign key to products
    quantity INT NOT NULL,  -- Quantity of the product ordered
    price DECIMAL(10, 2) NOT NULL  -- Price of the product at the time of the order
);

-- 6. Inventory table (tracks inventory movements)
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,  -- Unique inventory ID
    product_id INT REFERENCES products(product_id),  -- Foreign key to products
    quantity_in INT NOT NULL,  -- Quantity added to inventory
    quantity_out INT NOT NULL,  -- Quantity removed from inventory
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of inventory transaction
);

-- 7. Manufacturing_Orders table (stores details of manufacturing orders)
CREATE TABLE manufacturing_orders (
    manufacturing_order_id SERIAL PRIMARY KEY,  -- Unique manufacturing order ID
    product_id INT REFERENCES products(product_id),  -- Foreign key to products
    quantity INT NOT NULL,  -- Quantity to be manufactured
    due_date TIMESTAMP,  -- Due date for manufacturing completion
    status VARCHAR(50) DEFAULT 'pending'  -- Manufacturing order status
);

-- 8. Raw_Materials table (stores raw materials used in manufacturing)
CREATE TABLE raw_materials (
    material_id SERIAL PRIMARY KEY,  -- Unique material ID
    material_name VARCHAR(255) NOT NULL,  -- Material name
    description TEXT,  -- Material description
    unit_price DECIMAL(10, 2),  -- Price per unit of material
    stock_quantity INT NOT NULL  -- Available stock quantity of material
);

-- 9. Manufacturing_Inventory table (tracks raw material usage in manufacturing)
CREATE TABLE manufacturing_inventory (
    manufacturing_inventory_id SERIAL PRIMARY KEY,  -- Unique ID
    material_id INT REFERENCES raw_materials(material_id),  -- Foreign key to raw materials
    quantity_used INT NOT NULL,  -- Quantity of material used
    manufacturing_order_id INT REFERENCES manufacturing_orders(manufacturing_order_id),  -- Foreign key to manufacturing orders
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Date of transaction
);

-- 10. Payments table (stores payments made by customers)
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,  -- Unique payment ID
    order_id INT REFERENCES orders(order_id),  -- Foreign key to orders
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Payment date
    amount DECIMAL(10, 2) NOT NULL,  -- Payment amount
    payment_method VARCHAR(50),  -- Payment method (e.g., credit card, bank transfer)
    status VARCHAR(50) DEFAULT 'completed'  -- Payment status
);

-- Insert sample customers
INSERT INTO customers (company_name, contact_name, contact_email, phone, address)
VALUES
('Acme Corp', 'John Doe', 'johndoe@acmecorp.com', '123-456-7890', '123 Elm St'),
('Beta Industries', 'Jane Smith', 'janesmith@betaind.com', '987-654-3210', '456 Oak St');

-- Insert sample products
INSERT INTO products (product_name, description, price, stock_quantity)
VALUES
('Widget A', 'High-quality widget', 25.99, 100),
('Widget B', 'Standard widget', 15.99, 200);

-- Insert sample suppliers
INSERT INTO suppliers (company_name, contact_name, contact_email, phone, address)
VALUES
('SupplyCo', 'Alice Brown', 'alice@supplyco.com', '123-111-2222', '789 Pine St'),
('PartsPlus', 'Bob Green', 'bob@partsplus.com', '321-654-9870', '101 Maple St');

-- Insert sample orders
INSERT INTO orders (customer_id, order_date, status, total_amount)
VALUES
(1, '2024-12-01', 'pending', 51.98),
(2, '2024-12-02', 'completed', 31.98);

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, price)
VALUES
(1, 1, 2, 25.99),
(2, 2, 2, 15.99);

-- Insert sample inventory transactions
INSERT INTO inventory (product_id, quantity_in, quantity_out)
VALUES
(1, 100, 0),
(2, 200, 50);

-- Insert sample manufacturing orders
INSERT INTO manufacturing_orders (product_id, quantity, due_date, status)
VALUES
(1, 50, '2024-12-15', 'pending'),
(2, 100, '2024-12-20', 'completed');

-- Insert raw materials
INSERT INTO raw_materials (material_name, description, unit_price, stock_quantity)
VALUES
('Steel', 'Raw steel for widgets', 5.50, 500),
('Plastic', 'Plastic for widget casing', 2.00, 300);

-- Insert sample manufacturing inventory transactions
INSERT INTO manufacturing_inventory (material_id, quantity_used, manufacturing_order_id)
VALUES
(1, 250, 1),
(2, 200, 2);

-- Insert sample payments
INSERT INTO payments (order_id, amount, payment_method, status)
VALUES
(1, 51.98, 'Credit Card', 'completed'),
(2, 31.98, 'Bank Transfer', 'completed');

-- Select all orders for a customer
SELECT * FROM orders WHERE customer_id = 1;

-- Select all products in an order
SELECT oi.order_item_id, p.product_name, oi.quantity, oi.price
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
WHERE oi.order_id = 1;

-- Select inventory details for a product
SELECT * FROM inventory WHERE product_id = 1;

-- Select manufacturing orders and their materials used
SELECT mo.manufacturing_order_id, p.product_name, mi.quantity_used, rm.material_name
FROM manufacturing_orders mo
JOIN products p ON mo.product_id = p.product_id
JOIN manufacturing_inventory mi ON mo.manufacturing_order_id = mi.manufacturing_order_id
JOIN raw_materials rm ON mi.material_id = rm.material_id;

-- Select payment details for an order
SELECT * FROM payments WHERE order_id = 1;
