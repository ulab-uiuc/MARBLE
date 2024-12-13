-- 1. Users table (stores information about users)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,  -- Unique user ID
    username VARCHAR(50) UNIQUE NOT NULL,  -- Username
    first_name VARCHAR(100),  -- User's first name
    last_name VARCHAR(100),   -- User's last name
    email VARCHAR(255) UNIQUE NOT NULL,  -- User email
    password VARCHAR(255) NOT NULL,  -- User password
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Account creation time
);

-- 2. Artists table (stores artist information)
CREATE TABLE artists (
    artist_id SERIAL PRIMARY KEY,  -- Unique artist ID
    name VARCHAR(255) NOT NULL,  -- Artist name
    bio TEXT,  -- Artist biography
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Artist creation time
);

-- 3. Albums table (stores album details)
CREATE TABLE albums (
    album_id SERIAL PRIMARY KEY,  -- Unique album ID
    artist_id INT REFERENCES artists(artist_id),  -- Foreign key to artists
    title VARCHAR(255) NOT NULL,  -- Album title
    release_date DATE,  -- Album release date
    genre VARCHAR(100),  -- Genre of the album
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Album creation time
);

-- 4. Songs table (stores song details)
CREATE TABLE songs (
    song_id SERIAL PRIMARY KEY,  -- Unique song ID
    album_id INT REFERENCES albums(album_id),  -- Foreign key to albums
    title VARCHAR(255) NOT NULL,  -- Song title
    duration INT,  -- Duration in seconds
    track_number INT,  -- Track number in the album
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Song creation time
);

-- 5. Playlists table (stores playlists created by users)
CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,  -- Unique playlist ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    name VARCHAR(255) NOT NULL,  -- Playlist name
    description TEXT,  -- Playlist description
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Playlist creation time
);

-- 6. Playlist_Songs table (stores songs in playlists)
CREATE TABLE playlist_songs (
    playlist_song_id SERIAL PRIMARY KEY,  -- Unique playlist song ID
    playlist_id INT REFERENCES playlists(playlist_id),  -- Foreign key to playlists
    song_id INT REFERENCES songs(song_id),  -- Foreign key to songs
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Song added to playlist time
);

-- 7. User_Activity table (stores users' listening activity)
CREATE TABLE user_activity (
    activity_id SERIAL PRIMARY KEY,  -- Unique activity ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    song_id INT REFERENCES songs(song_id),  -- Foreign key to songs
    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Time song was played
);

-- 8. Subscriptions table (stores subscription details for users)
CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,  -- Unique subscription ID
    user_id INT REFERENCES users(user_id),  -- Foreign key to users
    start_date DATE,  -- Subscription start date
    end_date DATE,  -- Subscription end date
    plan_type VARCHAR(50),  -- Subscription plan (e.g., free, premium)
    status VARCHAR(50) DEFAULT 'active'  -- Subscription status
);

-- 9. Payments table (stores payment information for subscriptions)
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,  -- Unique payment ID
    subscription_id INT REFERENCES subscriptions(subscription_id),  -- Foreign key to subscriptions
    amount DECIMAL(10, 2) NOT NULL,  -- Payment amount
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Payment date
    payment_method VARCHAR(50),  -- Payment method (e.g., credit card, PayPal)
    status VARCHAR(50) DEFAULT 'completed'  -- Payment status
);

-- Insert sample users
INSERT INTO users (username, first_name, last_name, email, password)
VALUES 
('johndoe', 'John', 'Doe', 'john.doe@example.com', 'password123'),
('janesmith', 'Jane', 'Smith', 'jane.smith@example.com', 'password456');

-- Insert sample artists
INSERT INTO artists (name, bio)
VALUES 
('Artist A', 'Bio of Artist A'),
('Artist B', 'Bio of Artist B');

-- Insert sample albums
INSERT INTO albums (artist_id, title, release_date, genre)
VALUES 
(1, 'Album A', '2024-01-01', 'Pop'),
(2, 'Album B', '2023-12-01', 'Rock');

-- Insert sample songs
INSERT INTO songs (album_id, title, duration, track_number)
VALUES 
(1, 'Song 1', 240, 1),
(1, 'Song 2', 210, 2),
(2, 'Song 3', 220, 1);

-- Insert sample playlists
INSERT INTO playlists (user_id, name, description)
VALUES 
(1, 'My Playlist', 'A playlist of my favorite songs'),
(2, 'Rock Playlist', 'A playlist for rock music');

-- Insert songs into playlists
INSERT INTO playlist_songs (playlist_id, song_id)
VALUES 
(1, 1),
(1, 2),
(2, 3);

-- Insert sample user activity
INSERT INTO user_activity (user_id, song_id)
VALUES 
(1, 1),
(1, 2),
(2, 3);

-- Insert sample subscriptions
INSERT INTO subscriptions (user_id, start_date, end_date, plan_type)
VALUES 
(1, '2024-01-01', '2025-01-01', 'premium'),
(2, '2023-12-01', '2024-12-01', 'free');

-- Insert sample payments
INSERT INTO payments (subscription_id, amount, payment_method, status)
VALUES 
(1, 99.99, 'Credit Card', 'completed'),
(2, 0.00, 'None', 'completed');

-- Select all songs in a specific playlist
SELECT ps.playlist_song_id, s.title, s.duration
FROM playlist_songs ps
JOIN songs s ON ps.song_id = s.song_id
WHERE ps.playlist_id = 1;

-- Select all activities of a user
SELECT ua.activity_id, s.title, ua.played_at
FROM user_activity ua
JOIN songs s ON ua.song_id = s.song_id
WHERE ua.user_id = 1;

-- Select all subscriptions for a user
SELECT * FROM subscriptions WHERE user_id = 1;

-- Select all payments for a subscription
SELECT * FROM payments WHERE subscription_id = 1;

-- Select all songs by a specific artist
SELECT s.title, s.duration
FROM songs s
JOIN albums a ON s.album_id = a.album_id
JOIN artists ar ON a.artist_id = ar.artist_id
WHERE ar.name = 'Artist A';
