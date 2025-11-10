-- HBnB: Test CRUD operations
-- ==========================

USE hbnb_task10;
SHOW TABLES;

-- User Table Tests
-- ==========================
-- Check that is_admin is true for Admin user
SELECT '* Check the is_admin value for the Admin user:' AS '** Test Info';
SELECT is_admin FROM users
WHERE first_name = 'Admin';

-- Add another user (non-admin)
SELECT '* Insert John Doe user and show all users:' AS '** Test Info';
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    'b67cfeec-f76b-4977-adbf-078ac9474633', -- random UUID
    'John',
    'Doe',
    'john.doe@gmail.com',
    '$2a$12$jJTWLL7W6LLceqzSBn6aU.rC2phnpRDL9GwHEyFvpJk1YENH7Uio6',  -- hashed "password123"
    FALSE 
);
SELECT * FROM users;

-- Update users name and email based on id
SELECT '* Update John Doe user to Jane Doe and show using id:' AS '** Test Info';
UPDATE users
SET first_name = 'Jane', email = 'jane.doe@gmail.com'
WHERE id = 'b67cfeec-f76b-4977-adbf-078ac9474633';
SELECT * FROM users
WHERE id = 'b67cfeec-f76b-4977-adbf-078ac9474633';

-- Delete user based on email
SELECT '* Delete Jane Doe user using email and show all users:' AS '** Test Info';
DELETE FROM users
WHERE email = 'jane.doe@gmail.com';
SELECT * FROM users;

