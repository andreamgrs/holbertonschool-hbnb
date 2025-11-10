-- HBnB: Schema Creation
-- ==========================

-- User Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "users" (
    id CHAR(36) PRIMARY KEY, -- this is the uuid
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE -- admin yes or no default to not admin first

);

-- Place Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "places" (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL, -- instruction for last task said user_id and now this task says owner_id
    --if user is deleted, all places referecing the user will be deleted
    CONSTRAINT places_foreignkey FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Review Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "reviews" (
    id CHAR(36) PRIMARY KEY,
    text VARCHAR(100) NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,


-- Amenity Table:
-- ==========================
CREATE TABLE IF NOT EXISTS "amenities" (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,

