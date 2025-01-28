-- 1. Users table (stores user information)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Unique user ID
    first_name VARCHAR(100) NOT NULL,  -- User's first name
    last_name VARCHAR(100) NOT NULL,  -- User's last name
    email VARCHAR(255) UNIQUE NOT NULL,  -- Unique email
    password_hash VARCHAR(255) NOT NULL,  -- Hashed password
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Account creation time
);

-- 2. Accounts table (stores financial account details)
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,  -- Unique account ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    account_type VARCHAR(50) NOT NULL,  -- Type of account (e.g., checking, savings)
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0,  -- Current balance
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Account creation time
);

-- 3. Transactions table (stores transaction details)
CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,  -- Unique transaction ID
    account_id INT REFERENCES accounts(account_id),  -- Foreign key to accounts
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of transaction
    transaction_type VARCHAR(50) NOT NULL,  -- Type of transaction (e.g., deposit, withdrawal)
    amount DECIMAL(15, 2) NOT NULL,  -- Transaction amount
    description TEXT  -- Description of the transaction
);

-- 4. Investments table (stores investment details)
CREATE TABLE investments (
    investment_id SERIAL PRIMARY KEY,  -- Unique investment ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    investment_name VARCHAR(255) NOT NULL,  -- Name of the investment
    amount DECIMAL(15, 2) NOT NULL,  -- Investment amount
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Investment date
);

-- 5. Investment_Transactions table (stores transactions for investments)
CREATE TABLE investment_transactions (
    investment_transaction_id SERIAL PRIMARY KEY,  -- Unique transaction ID
    investment_id INT REFERENCES investments(investment_id),  -- Foreign key to investments
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Date of the transaction
    transaction_type VARCHAR(50) NOT NULL,  -- Type of transaction (e.g., buy, sell)
    amount DECIMAL(15, 2) NOT NULL,  -- Amount of the transaction
    price DECIMAL(15, 2) NOT NULL  -- Price per unit at the time of the transaction
);

-- Insert sample users
INSERT INTO users (first_name, last_name, email, password_hash)
VALUES
('John', 'Doe', 'john.doe@example.com', 'hashed_password_1'),
('Jane', 'Smith', 'jane.smith@example.com', 'hashed_password_2');

-- Insert sample accounts
INSERT INTO accounts (user_id, account_type, balance)
VALUES
(1, 'checking', 1000.00),
(1, 'savings', 5000.00),
(2, 'checking', 1500.00);

-- Insert sample transactions for John
INSERT INTO transactions (account_id, transaction_type, amount, description)
VALUES
(1, 'deposit', 500.00, 'Salary deposit'),
(1, 'withdrawal', 200.00, 'ATM withdrawal'),
(2, 'deposit', 1000.00, 'Transfer from savings');

-- Insert sample investments for John
INSERT INTO investments (user_id, investment_name, amount)
VALUES
(1, 'Stocks', 1000.00),
(1, 'Bonds', 3000.00);

-- Insert sample investment transactions for John
INSERT INTO investment_transactions (investment_id, transaction_type, amount, price)
VALUES
(1, 'buy', 1000.00, 50.00),  -- John buys 20 stocks at $50 each
(1, 'sell', 500.00, 60.00);  -- John sells 10 stocks at $60 each

-- Query to retrieve account details for a user
SELECT a.account_id, a.account_type, a.balance
FROM accounts a
JOIN users u ON a.user_id = u.user_id
WHERE u.user_id = 1;  -- Accounts for John

-- Query to retrieve all transactions for a user
SELECT t.transaction_id, t.transaction_date, t.transaction_type, t.amount, t.description
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
WHERE a.user_id = 1;  -- Transactions for John

-- Query to retrieve all investments for a user
SELECT i.investment_id, i.investment_name, i.amount
FROM investments i
WHERE i.user_id = 1;  -- Investments for John

-- Query to retrieve all investment transactions for a user
SELECT it.investment_transaction_id, it.transaction_date, it.transaction_type, it.amount, it.price
FROM investment_transactions it
JOIN investments i ON it.investment_id = i.investment_id
WHERE i.user_id = 1;  -- Investment transactions for John

-- Query to calculate the total balance of a user's accounts
SELECT u.first_name, u.last_name, SUM(a.balance) AS total_balance
FROM users u
JOIN accounts a ON u.user_id = a.user_id
GROUP BY u.user_id;

-- Query to calculate the total amount of investments for a user
SELECT u.first_name, u.last_name, SUM(i.amount) AS total_investments
FROM users u
JOIN investments i ON u.user_id = i.user_id
GROUP BY u.user_id;

-- Query to calculate profit/loss for a specific investment (stocks in this case)
SELECT i.investment_name, SUM(it.amount * it.price) AS total_value, i.amount AS initial_investment,
       (SUM(it.amount * it.price) - i.amount) AS profit_or_loss
FROM investment_transactions it
JOIN investments i ON it.investment_id = i.investment_id
WHERE i.investment_name = 'Stocks'
GROUP BY i.investment_name, i.amount;
