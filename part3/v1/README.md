# 🏠 HBnB Project 

## Part 3 Enhanced Backend with Authentication and Database Integration

In this Part 3 of the HBnB Project we focus on transforming the backend into a secure, persistent, and production-ready system. Where we implement user authentication, enforce access control, and migrate from in-memory storage to a robust database architecture using SQLAlchemy and SQLite with MySQL prepared for deployment.

### 🧱 Project Summary
- Add password hashing to User model with bcrypt2
- Secure API with JWT authentication (Flask-JWT-Extended)
- Implement role-based access control (is_admin)
- Replace in-memory storage with SQLite using SQLAlchemy
- Map models (User, Place, Review, Amenity) to database tables
- Configure MySQL for production use
- Visualize schema with mermaid.js diagrams

#### 🔐 Access Control Overview

Only authenticated users can perform actions tied to their ownership:
- Create, update, and delete their own places
- Create and update reviews, with checks to prevent reviewing their own places or submitting duplicates
- Modify their user profile (excluding email and password)

Admin users have elevated privileges:
- Create new users
- Modify any user’s data, including email and password (with unique email validation)
- Add and update amenities
- Bypass ownership restrictions on places and reviews

#### Project Structure

```
v1/
|-- README.md
|-- app
|   |-- __init__.py
|   |-- api
|   |   |-- __init__.py
|   |   `-- v1
|   |       |-- __init__.py
|   |       |-- admin.py
|   |       |-- amenities.py
|   |       |-- auth.py
|   |       |-- places.py
|   |       |-- reviews.py
|   |       `-- users.py
|   |-- models
|   |   |-- __init__.py
|   |   |-- amenity.py
|   |   |-- base.py
|   |   |-- place.py
|   |   |-- review.py
|   |   `-- user.py
|   |-- persistence
|   |   |-- __init__.py
|   |   |-- amenity_repository.py
|   |   |-- place_repository.py
|   |   |-- repository.py
|   |   |-- review_repository.py
|   |   `-- user_repository.py
|   |-- services
|   |   |-- __init__.py
|   |   `-- facade.py
|   `-- tests
|       |-- __init__.py
|       |-- api_unittest_amenity.py
|       |-- api_unittest_places.py
|       |-- api_unittest_review.py
|       |-- api_unittest_users.py
|       |-- class_model_amenity_test.py
|       |-- class_model_review_test.py
|       |-- class_models_place_test.py
|       |-- class_models_test.py
|       |-- doc_api_unittest_places.txt
|       |-- facade_unittest_amenity.py
|       |-- facade_unittest_places.py
|       |-- facade_unittest_review.py
|       `-- facade_unittest_user.py
|-- config.py
|-- entity_relationship_diagram.svg
|-- requirements.txt
|-- run.py
`-- sql
      |-- create_database.sql
      `-- test_operations.sql
```

### 🛠️ Installation and running
#### Clone the repository and make sure to have python3 installed
```bash
git clone https://github.com/andreamgrs/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

#### Install requirements
Navigate to the part3 directory, folder v1. 
```bash
cd part3/v1
pip install -r requirements.txt
```

#### To initialize the database and create the table, run:
```bash
python3 -m flask --app run shell
>>> from app import db
>>> db.create_all()
```

#### Run the application inside v1

```bash
python3 run.py
```

The API will now be running at:
```bash
http://127.0.0.1:5000/api/v1/
```

#### Create first admin user
When the system has no users yet, the system lets you create the first user without an admin token. However, after this, in order to test creating another user, creating an amenity, or modify a user, etc, we need an admin autorisation token (aka login as an admin). 

For this reason, the first user must be an admin. You must set is_admin = TRUE when creating the first user. 

**For example:**

POST /api/v1/users/ endpoint
```bash
{
   "first_name": "Tom",
    "last_name": "Doe",
    "email": "tom@example.com",
    "password": "your_password1",
    "is_admin": true
}
```

#### Get authorisation token for admin user:
Log in using the admin details to generate an authorisation token. This token will be required to perform subsequent admin only actions.

**For example:**

POST /api/v1/auth/login endpoint
```bash
{
   "email": "tom@example.com",
   "password": "your_password1"
}
```

### 🚀 Swagger documentation
Once you run the application, you can access the swagger documentation. 

Eg: http://127.0.0.1:5000/api/v1/

**IMPORTANT:** Test API endpoints using CURLS/POSTMAN 

### API Endpoints

#### Admin

      1. POST /api/v1/users/  - Admin can register new users
      2. PUT /api/v1/users/{user_id}  - Admin can update user information
      3. POST /api/v1/amenities/ - Admin can create amenities
      4. PUT /api/v1/amenities/{amenity_id} - Admin can update amenity

#### Login

      1. POST /api/v1/auth/login - Any user can login with email and password
      2. GET /api/v1/auth/protected - A protected endpoint that requires JWT token

#### Users

      1. GET /api/v1/users/  - Get all existing users
      2. GET /api/v1/users/{user_id}  - Get user details

#### Places

      1. POST /api/v1/places/  - Create a new place
      2. GET /api/v1/places/   - Get all places
      3. GET /api/v1/places/{place_id} - Get place details
      4. PUT /api/v1/places/{place_id}  - Update place information
      5. DELETE /api/v1/places/{place_id} - Delete a place

#### Amenities

      1. GET /api/v1/amenities/ - Get all amenities
      2. GET /api/v1/amenities/{amenity_id} - Get amenity details
      3. DELETE /api/v1/amenities/{amenity_id} - Admin can delete any amenity

#### Reviews

      1. POST /api/v1/reviews/ - Create review
      2. GET /api/v1/reviews/ - Get all reviews
      3. GET /api/v1/reviews/{review_id} - Get review details
      4. PUT /api/v1/reviews/{review_id} - Update review
      5. DELETE /api/v1/reviews/{review_id} - Delete review

### Endpoint Examples
#### Create a place:
You need authorization token from the owner of the place to create a place. Admin can bypass this restriction.

POST to /api/v1/places/ endpoint

**Request Body**
```bash
{
   "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "<user_id>",
    "amenities": []
}
```
#### Create a new user in order to get a review (the owner of the place cannot make a review):
POST to /api/v1/users/ endpoint

**Request Body**
```bash
{
   "first_name": "Ally",
    "last_name": "Doe",
    "email": "ally@example.com",
    "password": "your_password1",
    "is_admin": false
}
```
#### Get token from new user:
POST to /api/v1/auth/login endpoint

**Request Body**
```bash
{
   "email": "ally@example.com",
    "password": "your_password1"
}
```
#### Create a new review:
POST to /api/v1/reviews/ endpoint

**Request Body**
```bash
{
  "text": "Great",
    "rating": 5,
    "user_id": "<user_id>",
    "place_id": "<place_id>"
}
```
#### Update review BY ID:

PUT to /api/v1/reviews/<review_id> endpoint

**Request Body**
```bash
{
  "text": "Not bad",
    "rating": 2
}
```
#### Get review
GET /api/v1/reviews/ endpoint

#### Delete review
DELETE /api/v1/reviews/<review_id> endpoint

### ⚙️ SQL Scripts for Table Generation and Initial Data

In order to run the scripts first:

Install MySQL on Ubuntu
```bash
sudo apt update
sudo apt install mysql-server
```
Start the SQL server
```bash
service mysql start
```
Run scripts
From the v1/sql folder
```bash
cat create_database.sql | mysql -uroot -p
cat test_operations.sql | mysql -uroot -p
```
Connect to your MySQL server, use query show databases to see the database hbnb_task10
```bash
sudo mysql
Welcome to the MySQL monitor...
mysql> show databases;
```
### 📝 Generate Database Diagrams
We have created Entity-Relationship (ER) diagrams to visually represent the structure of the database schema for the HBnB project using Mermaid.js.

- USER entity has a one-to-many relationship with PLACE, meaning each user (admin) can create multiple places, but each place is owned by a single user. 
- PLACE and AMENITY entities are connected through a many-to-many relationship, implemented via the PLACE_AMENITY join table. Each place can have multiple amenities, and each amenity is associated with multiple places.
- USER has one-to-many relationship with REVIEW, a user can write multiple reviews. 
- PLACE has one-to-many relationship with REVIEW, each place can receive multiple reviews. 

This setup enables users to review different places, and places to accumulate feedback from various users.

For bookings or reservations:
- USER has a one-to-many relationship with BOOKING, an user can make multiple bookings.
- PLACE has a one-to-many relationship with BOOKING, allowing each place to be booked multiple times by different users.

You can view our diagram using the file entity_relationship_diagram.svg

## 👥 Contributors
- Thannie Phan
- Sheeny Soulsby
- Andrea Munoz
