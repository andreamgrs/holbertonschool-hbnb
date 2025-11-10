-- HBnB: Table generation & Initial Data
-- ==========================

DROP DATABASE IF EXISTS hbnb_task10; /*Deletes the database*/
CREATE DATABASE IF NOT EXISTS hbnb_task10;
USE hbnb_task10;


-- User Table:
-- ==========================
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY, /* this is the uuid */
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE /* admin yes or no default to not admin first */
    );

-- Place Table:
-- ==========================
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL, /* instruction for last task said user_id and now this task says owner_id */
    FOREIGN KEY (owner_id) REFERENCES users(id) /* if user is deleted, all places referecing the user will be deleted */
);


-- Review Table:
-- ==========================
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,

    CONSTRAINT unique_user UNIQUE(user_id, place_id) /* this is equal to 1 user 1 place 1 review only */
);


-- Amenity Table:
-- ==========================
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);


-- Place_Amenity Table:
-- ==========================
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,

    CONSTRAINT pk_place_amenity PRIMARY KEY (place_id, amenity_id), -- to ensure we don't have the same amenities in the same place?

    -- Foreign key linking to places
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,

    -- Foreign key linking to amenities
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);



-- INSERT DATA - ADMIN USER:
-- ==========================

INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$kzLS9yiGxauc9OOvXqF9y.SwuqicVGrFWTk7IWnnks7cG95pnVUMa',  -- hashed password
    TRUE
);


-- INSERT DATA - CREATE INITIAL AMENITIES:
-- ==========================

INSERT INTO amenities (id, name) VALUES
('8b44d013-1adf-4688-b776-d6293680af13', 'WiFi'),
('bc5c25ac-48de-489f-a41f-ec7d762fa38a', 'Swimming Pool'),
('fbd0f8d0-800d-481d-9867-e6ee206ad110', 'Air Conditioning');

-- INSERT DATA PLACE FOR REVIEW:
-- ==========================

INSERT INTO places (id, title, description, price, latitude, longitude, owner_id) VALUES (
    'cadb7beb-a956-45f0-9a68-933d450ba490', -- id (random UUID)
    'Cozy Apartment', -- title
    'A nice place to stay', -- description
    100.0, -- price
    37.7749, -- latitude
    -122.4194, -- longitude
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1' -- owner id (admin user)
);