-- HBnB: Test Inital Data and CRUD operations
-- ==========================
SELECT '* List tables in database' AS '** HBnB Database Tests';
USE hbnb_task10;
SHOW TABLES;

-- Check that is_admin is true for Admin user
SELECT '* Check the is_admin value is TRUE for the Admin user:' AS '** Inital Data Tests';
SELECT is_admin FROM users
WHERE first_name = 'Admin';

SELECT '* Check the amenities (WiFi, Swimming Pool, and Air Conditioning) are inserted properly:' AS '** Initial Data Tests';
SELECT * FROM amenities;

-- User Table CRUD Tests
-- ==========================
-- Create another user (non-admin)
SELECT '* Insert John Doe user.' AS '** User Tests';
INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    'b67cfeec-f76b-4977-adbf-078ac9474633', -- random UUID
    'John',
    'Doe',
    'john.doe@gmail.com',
    '$2a$12$jJTWLL7W6LLceqzSBn6aU.rC2phnpRDL9GwHEyFvpJk1YENH7Uio6',  -- hashed "password123"
    FALSE 
);

-- Retreive all users
SELECT '* List all users:' AS '** User Tests';
SELECT * FROM users;

-- Update users name and email based on id
SELECT '* Update John Doe user to Jane Doe and list user using id:' AS '** User Tests';
UPDATE users
SET first_name = 'Jane', email = 'jane.doe@gmail.com'
WHERE id = 'b67cfeec-f76b-4977-adbf-078ac9474633';
SELECT * FROM users
WHERE id = 'b67cfeec-f76b-4977-adbf-078ac9474633';

-- Delete user based on email
SELECT '* Delete Jane Doe user using email and list all users:' AS '** User Tests';
DELETE FROM users
WHERE email = 'jane.doe@gmail.com';
SELECT * FROM users;


-- Place Table Tests
-- ==========================
-- Create a place
SELECT '* Insert new place (Cozy Apartment).' AS '** Place Tests';
INSERT INTO places
VALUES (
    '8bcce66e-2008-4b78-813f-c0ff37804e35', -- id (random UUID)
    'Cozy Apartment', -- title
    'A nice place to stay', -- description
    100.0, -- price
    37.7749, -- latitude
    -122.4194, -- longitude
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1' -- owner id (admin user)
);

-- Retreive all places
SELECT '* List all places:' AS '** Place Tests';
SELECT * FROM places;

-- Create another place
SELECT '* Insert new place (Family Home).' AS '** Place Tests';
INSERT INTO places
VALUES (
    '6017b234-adeb-4a42-b075-3a35096c34cf', -- id (random UUID)
    'Family Home', -- title
    'Ideal for family holidays', -- description
    200.0, -- price
    33.1, -- latitude
    50.5, -- longitude
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1' -- owner id (admin user)
);

-- Retreive all places
SELECT '* List all places:' AS '** Place Tests';
SELECT * FROM places;

-- Update place name based on id
SELECT '* Update Cozy Apartment using id and list all place using id' AS '** Place Tests';
UPDATE places
SET title = 'Luxury Apartment', price = '150'
WHERE id = '8bcce66e-2008-4b78-813f-c0ff37804e35';
SELECT * FROM places
WHERE id = '8bcce66e-2008-4b78-813f-c0ff37804e35';

-- Delete place based on id
SELECT '* Delete Cozy Apartment using id and list all places:' AS '** Places Tests';
DELETE FROM places
WHERE id = '8bcce66e-2008-4b78-813f-c0ff37804e35';
SELECT * FROM places;