-- INSERT DATA - CREATE ADMIN USER:
-- ==========================

INSERT INTO users (id, _first_name, _last_name, _email, _password, _is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2a$12$8/E0z8pBnJD6zgOpgEUkW.EmsnfIlqo1E8Csrg0Pdo9.EBEoWrgUS',  -- hashed password
    TRUE
);

-- INSERT DATA - CREATE INITIAL AMENITIES:
-- ==========================

INSERT INTO amenities (id, _name) VALUES 
('8b44d013-1adf-4688-b776-d6293680af13', 'WiFi'),
('bc5c25ac-48de-489f-a41f-ec7d762fa38a', 'Swimming Pool'),
('fbd0f8d0-800d-481d-9867-e6ee206ad110', 'Air Conditioning');

