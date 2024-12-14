-- 1. Users table (stores information about users)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Unique user ID
    username VARCHAR(50) UNIQUE NOT NULL,  -- Username
    first_name VARCHAR(100),  -- User's first name
    last_name VARCHAR(100),   -- User's last name
    email VARCHAR(255) UNIQUE NOT NULL,  -- User email
    password VARCHAR(255) NOT NULL,  -- User password
    bio TEXT,  -- User's biography
    profile_picture VARCHAR(255),  -- URL to profile picture
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Account creation time
);

-- 2. Posts table (stores user posts)
CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,  -- Unique post ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    content TEXT,  -- Post content
    image_url VARCHAR(255),  -- URL to image associated with post
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Post creation time
    updated_at TIMESTAMP  -- Post last updated time
);

-- 3. Comments table (stores comments on posts)
CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,  -- Unique comment ID
    post_id INT REFERENCES posts(post_id) ON DELETE CASCADE,  -- Foreign key to posts
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    content TEXT NOT NULL,  -- Comment content
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Comment creation time
);

-- 4. Likes table (stores likes on posts)
CREATE TABLE likes (
    like_id SERIAL PRIMARY KEY,  -- Unique like ID
    post_id INT REFERENCES posts(post_id) ON DELETE CASCADE,  -- Foreign key to posts
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Like timestamp
);

-- 5. Followers table (stores follow relationships between users)
CREATE TABLE followers (
    follower_id INT REFERENCES users(user_id),  -- User who follows
    followed_id INT REFERENCES users(user_id),  -- User being followed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Follow time
    PRIMARY KEY (follower_id, followed_id)  -- Composite primary key
);

-- 6. Messages table (stores direct messages between users)
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,  -- Unique message ID
    sender_id INT REFERENCES users(user_id),  -- User who sent the message
    receiver_id INT REFERENCES users(user_id),  -- User who received the message
    content TEXT,  -- Message content
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Message sent time
    read_status BOOLEAN DEFAULT FALSE  -- Read status of the message
);

-- 7. Media table (stores media files associated with posts and messages)
CREATE TABLE media (
    media_id SERIAL PRIMARY KEY,  -- Unique media ID
    user_id INT REFERENCES users(user_id),  -- User who uploaded the media
    media_type VARCHAR(50) NOT NULL,  -- Type of media (image, video, etc.)
    media_url VARCHAR(255) NOT NULL,  -- URL to the media file
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Upload time
);

-- Insert some sample users
INSERT INTO users (username, first_name, last_name, email, password) 
VALUES 
('john_doe', 'John', 'Doe', 'john.doe@example.com', 'password123'),
('jane_smith', 'Jane', 'Smith', 'jane.smith@example.com', 'password456');

-- Insert some posts
INSERT INTO posts (user_id, content, image_url) 
VALUES 
(1, 'Excited to be part of this platform!', 'https://example.com/images/welcome.jpg'),
(2, 'Good morning, everyone!', 'https://example.com/images/morning.jpg');

-- Insert comments on posts
INSERT INTO comments (post_id, user_id, content) 
VALUES 
(1, 2, 'Welcome to the platform, John!'),
(2, 1, 'Good morning, Jane!');

-- Insert likes on posts
INSERT INTO likes (post_id, user_id) 
VALUES 
(1, 2),
(2, 1);

-- Insert follow relationships
INSERT INTO followers (follower_id, followed_id) 
VALUES 
(1, 2),  -- John follows Jane
(2, 1);  -- Jane follows John

-- Insert direct messages
INSERT INTO messages (sender_id, receiver_id, content) 
VALUES 
(1, 2, 'Hi Jane, how are you?'),
(2, 1, 'Im good, John! How about you?');

-- Insert media uploaded by users
INSERT INTO media (user_id, media_type, media_url) 
VALUES 
(1, 'image', 'https://example.com/media/photo1.jpg'),
(2, 'video', 'https://example.com/media/video1.mp4');

-- Select all posts along with user details
SELECT p.post_id, p.content, u.username, p.created_at
FROM posts p
JOIN users u ON p.user_id = u.user_id;

-- Select comments on a post
SELECT c.comment_id, c.content, u.username, c.created_at
FROM comments c
JOIN users u ON c.user_id = u.user_id
WHERE c.post_id = 1;

-- Select all likes on a post
SELECT l.like_id, u.username, l.created_at
FROM likes l
JOIN users u ON l.user_id = u.user_id
WHERE l.post_id = 1;

-- Select all followers of a user
SELECT u.username
FROM followers f
JOIN users u ON f.follower_id = u.user_id
WHERE f.followed_id = 1;

-- Select all direct messages between two users
SELECT m.content, u1.username AS sender, u2.username AS receiver, m.created_at
FROM messages m
JOIN users u1 ON m.sender_id = u1.user_id
JOIN users u2 ON m.receiver_id = u2.user_id
WHERE m.sender_id = 1 AND m.receiver_id = 2;
