-- 1. Users table (stores user information)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Unique user ID
    username VARCHAR(100) UNIQUE NOT NULL,  -- Unique username
    email VARCHAR(255) UNIQUE NOT NULL,  -- Unique email
    password_hash VARCHAR(255) NOT NULL,  -- Hashed password
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Account creation time
);

-- 2. Files table (stores file details)
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,  -- Unique file ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    file_name VARCHAR(255) NOT NULL,  -- File name
    file_path TEXT NOT NULL,  -- Path to the file on the server
    file_size BIGINT NOT NULL,  -- Size of the file in bytes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Upload time
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Last modification time
);

-- 3. Shared_Files table (stores files shared with other users)
CREATE TABLE shared_files (
    share_id SERIAL PRIMARY KEY,  -- Unique share ID
    file_id INT REFERENCES files(file_id),  -- Foreign key to files
    owner_id INT REFERENCES users(user_id),  -- Foreign key to owner (user who shared)
    shared_with INT REFERENCES users(user_id),  -- Foreign key to the user the file is shared with
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time the file was shared
    permissions VARCHAR(50) DEFAULT 'read'  -- Permissions (e.g., 'read', 'write')
);

-- 4. File_Access_Logs table (stores logs of file access)
CREATE TABLE file_access_logs (
    log_id SERIAL PRIMARY KEY,  -- Unique log ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    file_id INT REFERENCES files(file_id),  -- Foreign key to files
    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Time the file was accessed
    action VARCHAR(50) NOT NULL,  -- Action (e.g., 'viewed', 'downloaded')
    ip_address VARCHAR(50)  -- IP address from which the file was accessed
);

-- Insert sample users
INSERT INTO users (username, email, password_hash) 
VALUES 
('john_doe', 'john.doe@example.com', 'hashed_password_1'),
('jane_smith', 'jane.smith@example.com', 'hashed_password_2');

-- Insert sample files for John
INSERT INTO files (user_id, file_name, file_path, file_size) 
VALUES 
(1, 'document1.pdf', '/files/john_doe/document1.pdf', 102400),
(1, 'image1.jpg', '/files/john_doe/image1.jpg', 204800);

-- Insert sample files for Jane
INSERT INTO files (user_id, file_name, file_path, file_size) 
VALUES 
(2, 'presentation.pptx', '/files/jane_smith/presentation.pptx', 512000);

-- Share files with other users
INSERT INTO shared_files (file_id, owner_id, shared_with, permissions) 
VALUES 
(1, 1, 2, 'read'),  -- John shares document1.pdf with Jane
(2, 1, 2, 'write');  -- John shares image1.jpg with Jane

-- Insert file access logs
INSERT INTO file_access_logs (user_id, file_id, action, ip_address) 
VALUES 
(2, 1, 'viewed', '192.168.1.1'),  -- Jane viewed document1.pdf
(2, 2, 'downloaded', '192.168.1.2');  -- Jane downloaded image1.jpg

-- Query to retrieve all shared files for a user
SELECT sf.share_id, f.file_name, u.username AS shared_by, sf.permissions 
FROM shared_files sf
JOIN files f ON sf.file_id = f.file_id
JOIN users u ON sf.owner_id = u.user_id
WHERE sf.shared_with = 2;  -- Files shared with Jane

-- Query to retrieve all file access logs for a user
SELECT u.username, f.file_name, fal.action, fal.access_time, fal.ip_address
FROM file_access_logs fal
JOIN users u ON fal.user_id = u.user_id
JOIN files f ON fal.file_id = f.file_id
WHERE u.user_id = 2;  -- Access logs for Jane

-- Query to list all files uploaded by a user
SELECT f.file_name, f.file_size, f.created_at
FROM files f
WHERE f.user_id = 1;  -- Files uploaded by John

-- Query to count how many times a file was accessed
SELECT f.file_name, COUNT(fal.log_id) AS access_count
FROM file_access_logs fal
JOIN files f ON fal.file_id = f.file_id
GROUP BY f.file_name;

-- Query to get all users who have shared files with a specific user
SELECT u.username, COUNT(sf.share_id) AS shared_files_count
FROM shared_files sf
JOIN users u ON sf.owner_id = u.user_id
WHERE sf.shared_with = 2  -- Files shared with Jane
GROUP BY u.username;
