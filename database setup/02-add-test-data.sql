-- =================================================================================
-- SQL DML Script for the Library Management System (Comprehensive Test Data)
-- =================================================================================

-- Select the correct database
USE `library_app`;

-- To make this script re-runnable, we will clear all existing data and reset auto-increment counters.
SET FOREIGN_KEY_CHECKS = 0; 
TRUNCATE TABLE `Loans`;
TRUNCATE TABLE `Book_Authors`;
TRUNCATE TABLE `Authors`;
TRUNCATE TABLE `Books`;
TRUNCATE TABLE `Borrowers`;
SET FOREIGN_KEY_CHECKS = 1;


-- =================================================================================
-- 1. Authors
-- =================================================================================
INSERT INTO `Authors` (`name`) VALUES
('George Orwell'),
('J.R.R. Tolkien'),
('Brian W. Kernighan'),
('Dennis M. Ritchie'),
('Andrew S. Tanenbaum'),
('J.K. Rowling');


-- =================================================================================
-- 2. Books
-- =================================================================================
INSERT INTO `Books` (`title`, `isbn`, `publication_year`, `book_type`, `genre`, `subject`, `status`) VALUES
('1984', '9780451524935', 1949, 'Novel', 'Dystopian', NULL, 'available'),
('The Lord of the Rings', '9780618640157', 1954, 'Novel', 'Fantasy', NULL, 'on_loan'),
('The Hobbit', '9780618260300', 1937, 'Novel', 'Fantasy', NULL, 'available'),
('The C Programming Language', '9780131103627', 1988, 'Textbook', NULL, 'Programming', 'on_loan'),
('Computer Networks', '9780132126953', 2010, 'Textbook', NULL, 'Computer Science', 'available'),
('Harry Potter and the Sorcerer''s Stone', '9780590353427', 1997, 'Novel', 'Fantasy', NULL, 'available');


-- =================================================================================
-- 3. Book_Authors
-- =================================================================================
INSERT INTO `Book_Authors` (`book_id`, `author_id`) VALUES
(1, 1),
(5, 5),
(6, 6),
(2, 2),
(3, 2),
(4, 3),
(4, 4);


-- =================================================================================
-- 4. Borrowers
-- =================================================================================
INSERT INTO `Borrowers` (`first_name`, `last_name`, `email`, `registration_date`) VALUES
('Alice', 'Wonderland', 'alice.w@example.com', '2023-01-10'),
('Bob', 'Builder', 'bob.b@example.com', '2023-02-20'),
('Tim', 'Mak', 'tmak0244@gmail.com', '2025-12-05');


-- =================================================================================
-- 5. Loans
-- =================================================================================
INSERT INTO `Loans` (`book_id`, `borrower_id`, `loan_date`, `due_date`, `return_date`) VALUES
(1, 1, '2023-08-10', '2023-08-24', '2023-08-22'),
(1, 2, '2023-09-05', '2023-09-19', '2023-09-18'),
(4, 2, '2023-10-20', '2023-11-03', NULL),
(2, 1, '2023-10-25', '2023-11-08', NULL);

-- =================================================================================
-- End of Script
-- =================================================================================


