CREATE DATABASE IF NOT EXISTS u1traspace;
USE u1traspace;

CREATE TABLE IF NOT EXISTS users (
    `user_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `email` varchar(100) UNIQUE NOT NULL,
    `username` varchar(30) NOT NULL,
    `password` varchar(162) UNIQUE NOT NULL,
    `join_date` int NOT NULL,
    `last_seen` int NOT NULL,
    `page_views` int NOT NULL DEFAULT 0,
    `visible` bool NOT NULL DEFAULT TRUE,
    `private` bool NOT NULL DEFAULT FALSE,
    `layout` enum('u1traspace', 'myspace', 'twitter') NOT NULL DEFAULT 'u1traspace',
    `about` varchar(4096) DEFAULT NULL,
    FULLTEXT KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS page_comments (
    `comment_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `page_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `author_id` int NOT NULL REFERENCES users(`user_id`) ON UPDATE CASCADE,
    `corpus` varchar(1024) NOT NULL,
    `date` int NOT NULL,
    `visible` bool NOT NULL DEFAULT TRUE,
    `approved` bool NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS blogs (
    `blog_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `author_id` int NOT NULL REFERENCES users (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    `title` varchar(60) NOT NULL,
    `corpus` varchar(4096) NOT NULL,
    `date` int NOT NULL,
    `visible` bool NOT NULL DEFAULT TRUE,
    FULLTEXT KEY `title` (`title`, `corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS blog_comments (
    `comment_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `blog_id` int NOT NULL REFERENCES blogs (`blog_id`) ON UPDATE CASCADE,
    `author_id` int NOT NULL,
    `corpus` varchar(1024) NOT NULL,
    `date` int NOT NULL,
    `visible` bool NOT NULL DEFAULT TRUE,
    `approved` bool NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS friends (
    `relationship_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `sender_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `recipient_id` int NOT NULL REFERENCES users(`user_id`) ON UPDATE CASCADE,
    `date` int NOT NULL,
    `approved` bool NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS messages (
    `message_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `sender_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `recipient_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `date` int NOT NULL,
    `corpus` varchar(2048) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS backend IDENTIFIED BY '*E29C602C71D87AF4F1FFE1FD62D0AEDD76A8AAEF';
GRANT USAGE ON users TO `backend`@`%`;
GRANT USAGE ON page_comments TO `backend`@`%`;
GRANT USAGE ON blogs TO `backend`@`%`;
GRANT USAGE ON blog_comments TO `backend`@`%`;
GRANT USAGE ON friends TO `backend`@`%`;
GRANT USAGE ON messages TO `backend`@`%`;