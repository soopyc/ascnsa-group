-- SQL DDL Script for the Library Management System
-- Course: Database Systems and Design
-- This script creates all the necessary tables, sets up primary and foreign keys,
-- and applies constraints to ensure data integrity.

-- To make the script runnable multiple times, we drop existing tables first.
-- The order is important due to foreign key constraints (drop dependent tables first).
DROP TABLE IF EXISTS `Loans`;
DROP TABLE IF EXISTS `Book_Authors`;
DROP TABLE IF EXISTS `Books`;
DROP TABLE IF EXISTS `Authors`;
DROP TABLE IF EXISTS `Borrowers`;


-- =================================================================================
-- Table: Authors
-- Stores information about book authors.
-- =================================================================================
CREATE TABLE `Authors` (
    `author_id` INT AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`author_id`)
);


-- =================================================================================
-- Table: Books
-- Stores information about each book in the library.
-- This table implements the EER specialization for Textbooks and Novels.
-- =================================================================================
CREATE TABLE `Books` (
    `book_id` INT AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `isbn` VARCHAR(13) NOT NULL UNIQUE,
    `publication_year` YEAR,
    `status` ENUM('available', 'on_loan') NOT NULL DEFAULT 'available',
    `book_type` ENUM('Novel', 'Textbook', 'Generic') NOT NULL,
    
    -- Specialization attributes (can be NULL if not applicable)
    `genre` VARCHAR(100),       -- For Novels
    `subject` VARCHAR(100),     -- For Textbooks
    
    PRIMARY KEY (`book_id`)
);


-- =================================================================================
-- Table: Book_Authors (Junction Table)
-- Manages the many-to-many relationship between Books and Authors.
-- =================================================================================
CREATE TABLE `Book_Authors` (
    `book_id` INT,
    `author_id` INT,
    PRIMARY KEY (`book_id`, `author_id`), -- Composite primary key
    FOREIGN KEY (`book_id`) REFERENCES `Books`(`book_id`) ON DELETE CASCADE,
    FOREIGN KEY (`author_id`) REFERENCES `Authors`(`author_id`) ON DELETE CASCADE
);


-- =================================================================================
-- Table: Borrowers
-- Stores information about library members.
-- =================================================================================
CREATE TABLE `Borrowers` (
    `borrower_id` INT AUTO_INCREMENT,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `registration_date` DATE NOT NULL,
    PRIMARY KEY (`borrower_id`)
);


-- =================================================================================
-- Table: Loans
-- Stores records of books being borrowed by members.
-- =================================================================================
CREATE TABLE `Loans` (
    `loan_id` INT AUTO_INCREMENT,
    `book_id` INT NOT NULL,
    `borrower_id` INT NOT NULL,
    `loan_date` DATE NOT NULL,
    `due_date` DATE NOT NULL,
    `return_date` DATE, -- Can be NULL if the book has not been returned yet
    
    PRIMARY KEY (`loan_id`),
    FOREIGN KEY (`book_id`) REFERENCES `Books`(`book_id`),
    FOREIGN KEY (`borrower_id`) REFERENCES `Borrowers`(`borrower_id`)
);

-- =================================================================================
-- End of Script
-- =================================================================================