# Create table for PhoneBook
DROP TABLE IF EXISTS phonebook;
CREATE TABLE phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20)
);

#. Create tables for Snake Game user and score tracking
DROP TABLE IF EXISTS user_score;
DROP TABLE IF EXISTS game_user;

CREATE TABLE game_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE user_score (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES game_user(id) ON DELETE CASCADE,
    level INTEGER NOT NULL,
    score INTEGER NOT NULL,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

# Insert example data into phonebook
INSERT INTO phonebook (name, phone) VALUES ('Alice', '123456');
INSERT INTO phonebook (name, phone) VALUES ('Bob', '789101');

