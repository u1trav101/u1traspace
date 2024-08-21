CREATE DATABASE IF NOT EXISTS u1traspace;
USE u1traspace;

CREATE TABLE IF NOT EXISTS users (
    `user_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `email` varchar(100) UNIQUE NOT NULL,
    `username` varchar(30) NOT NULL,
    `password` varchar(162) UNIQUE NOT NULL,
    `join_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `last_seen` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `visible` bool NOT NULL DEFAULT TRUE,
    `approved` bool NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS blogs (
    `blog_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `author_id` int NOT NULL REFERENCES users (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    `title` varchar(60) NOT NULL,
    `corpus` varchar(4096) NOT NULL,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `visible` bool NOT NULL DEFAULT TRUE,
    FULLTEXT KEY `title` (`title`, `corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS blog_comments (
    `comment_id` int UNIQUE NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `blog_id` int NOT NULL REFERENCES blogs (`blog_id`) ON UPDATE CASCADE,
    `author_id` int NOT NULL,
    `corpus` varchar(1024) NOT NULL,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `visible` bool NOT NULL DEFAULT TRUE,
    `approved` bool NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS friends (
    `friend_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `sender_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `recipient_id` int NOT NULL REFERENCES users(`user_id`) ON UPDATE CASCADE,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `approved` bool NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS messages (
    `message_id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `sender_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `recipient_id` int NOT NULL REFERENCES users (`user_id`) ON UPDATE CASCADE,
    `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `corpus` varchar(2048) NOT NULL,
    `read` bool NOT NULL DEFAULT FALSE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

DELIMITER //
DROP PROCEDURE IF EXISTS update_last_seen;
CREATE PROCEDURE IF NOT EXISTS update_last_seen(parameter_user_id int)
    MODIFIES SQL DATA
    UPDATE users
    SET last_seen = CURRENT_TIMESTAMP
    WHERE user_id = parameter_user_id;
//

DROP PROCEDURE IF EXISTS increase_page_views;
CREATE PROCEDURE increase_page_views(parameter_user_id int)
    MODIFIES SQL DATA
    UPDATE users
    SET page_views = page_views + 1
    WHERE user_id = parameter_user_id
//

DROP TRIGGER IF EXISTS set_page_comment_approval;
CREATE TRIGGER set_page_comment_approval
BEFORE INSERT ON page_comments FOR EACH ROW
BEGIN
    DECLARE is_private bool;
    SET is_private = (
        SELECT private
        FROM users
        WHERE user_id = NEW.page_id
        LIMIT 1
    );

    SET NEW.approved = CASE is_private
        WHEN 0 THEN 1
    END;
END;
//

DROP TRIGGER IF EXISTS set_blog_comment_approval;
CREATE TRIGGER set_blog_comment_approval
BEFORE INSERT ON blog_comments FOR EACH ROW
BEGIN
    DECLARE is_private bool;
    SET is_private = (
        SELECT private
        FROM users
        WHERE user_id = (
            SELECT author_id
            FROM blogs
            WHERE blog_id = NEW.blog_id
        )
        LIMIT 1
    );

    SET NEW.approved = CASE is_private
        WHEN 0 THEN 1
    END;
END;
//
DELIMITER ;

CREATE USER IF NOT EXISTS 'backend'@'localhost' IDENTIFIED WITH mysql_native_password AS '*42FCEC4876A794A22B58238AEFC8E182E1899739';
CREATE USER IF NOT EXISTS 'backend'@'127.0.0.1' IDENTIFIED WITH mysql_native_password AS '*42FCEC4876A794A22B58238AEFC8E182E1899739';
CREATE USER IF NOT EXISTS 'backend'@'%' IDENTIFIED WITH mysql_native_password AS '*42FCEC4876A794A22B58238AEFC8E182E1899739';

GRANT INSERT, SELECT, DELETE, UPDATE, EXECUTE ON u1traspace.* TO 'backend'@'localhost';
GRANT INSERT, SELECT, DELETE, UPDATE, EXECUTE ON u1traspace.* TO 'backend'@'127.0.0.1';
GRANT INSERT, SELECT, DELETE, UPDATE, EXECUTE ON u1traspace.* TO 'backend'@'%';

FLUSH PRIVILEGES;
