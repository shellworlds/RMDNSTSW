CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email, first_name, last_name) 
VALUES 
    ('admin', 'admin@example.com', 'Admin', 'User'),
    ('john_doe', 'john@example.com', 'John', 'Doe'),
    ('jane_smith', 'jane@example.com', 'Jane', 'Smith');
