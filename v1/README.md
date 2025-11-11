# 🏠 HBnB Project 

## Part 3 Enhanced Backend with Authentication and Database Integration

In this Part 3 of the HBnB Project we focus on transforming the backend into a secure, persistent, and production-ready system. Where we implement user authentication, enforce access control, and migrate from in-memory storage to a robust database architecture using SQLAlchemy and SQLite with MySQL prepared for deployment.

### 🧱 Project Structure Summary
- Add password hashing to User model with bcrypt2
- Secure API with JWT authentication (Flask-JWT-Extended)
- Implement role-based access control (is_admin)
- Replace in-memory storage with SQLite using SQLAlchemy
- Map models (User, Place, Review, Amenity) to database tables
- Configure MySQL for production use
- Visualize schema with mermaid.js diagrams

### 🛠 Installation and running

#### Install requirements
```bash
pip install -r requirements.txt
pip install flask-bcrypt
```
#### Run the application

```bash
python3 run.py
```

#### To initialize the database and create the table, run:
```bash
python3 -m flask --app run shell
>>> from app import db
>>> db.create_all()
```
### 🧪 Swagger documentation
Once you run the application, you can access the swagger documentation. 
Eg: http://127.0.0.1:5000/api/v1/


### 🧪 Testing (using Postman/cURL)

Prior to test: When you create a user for the first time, that user need to be an admin in order to perform certain subsequent tasks later on. "is_admin" needs to be true when creating the first ever user. 

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


#### Test user creation and retrieval using Postman or cURL. For example, create a first ever new user:
The initial user must be an admin. To create additional users, you need to include the admin's Authorization Bearer token in the request header.
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{
   "first_name": "Tom",
    "last_name": "Doe",
    "email": "tom@example.com",
    "password": "your_password1",
    "is_admin": true
}'
```

#### Get token from ADMIN:
```bash
curl -X POST "http://localhost:5000/api/v1/auth/login" -H "Content-Type: application/json" -d '{
   "email": "tom@example.com",
    "password": "your_password1"
}'
```

#### Create a place:
You need authorization token from the owner of the place to create a place. Admin can bypass this restriction.
```bash
curl -X POST "http://localhost:5000/api/v1/places/" -H "Authorization: Bearer <user/admin_token>" -H "Content-Type: application/json" -d '{
   "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "<user_id>",
    "amenities": []
}'
```
#### Create a new user in order to get a review (the owner of the place cannot make a review):
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Authorization: Bearer <admin_token>" -H "Content-Type: application/json" -d '{
   "first_name": "Ally",
    "last_name": "Doe",
    "email": "ally@example.com",
    "password": "your_password1",
    "is_admin": false
}'
```
#### Get token from new user:
```bash
curl -X POST "http://localhost:5000/api/v1/auth/login" -H "Content-Type: application/json" -d '{
   "email": "ally@example.com",
    "password": "your_password1"
}'
```
#### Create a new review:
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" -H "Authorization: Bearer <new_user_token>" -H "Content-Type: application/json" -d '{
  "text": "Great",
    "rating": 5,
    "user_id": "<user_id>",
    "place_id": "<place_id>"
}'
```
#### Update review BY ID:
```bash
curl -X PUT "http://127.0.0.1:5000/api/v1/reviews/<review_id>" -H "Authorization: Bearer <new_user_token/admin_token>" -H "Content-Type: application/json" -d '{
  "text": "Not bad",
    "rating": 2
}'
```
#### Get review
```bash
curl -X GET "http://127.0.0.1:5000/api/v1/reviews/"
```
#### Delete review
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<review_id>" -H "Authorization: Bearer <new_user_token/admin_token>"
```

### 🧪 SQL Scripts for Table Generation and Initial Data

In order to run the scripts first:

Install MySQL on Ubuntu
```bash
sudo apt update
sudo apt install mysql-server
```
Run scripts
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
### Generate Database Diagrams
Entity-Relationship (ER) diagrams to visually represent the structure of the database schema for the HBnB project using Mermaid.js.

- USER entity has a one-to-many relationship with PLACE, meaning each user (admin) can create multiple places, but each place is owned by a single user. 
- PLACE and AMENITY entities are connected through a many-to-many relationship, implemented via the PLACE_AMENITY join table. This allows each place to have multiple amenities, and each amenity to be associated with multiple places.
- USER has one-to-many relationship with REVIEW, a user can write multiple reviews. 
- PLACE has one-to-many relationship with REVIEW, each place can receive multiple reviews. 

This setup enables users to review different places, and places to accumulate feedback from various users.

For bookings or reservations:
- USER has a one-to-many relationship with BOOKING, an user can make multiple bookings.
- PLACE has a one-to-many relationship with BOOKING, allowing each place to be booked multiple times by different users.


## Part 2 Implementation of Business Logic and API Endpoints

Implements HBnB Evolution’s backend using Python and Flask.

- Core models (User, Place, Review, Amenity)
- RESTful API endpoints with flask-restx.
- Layered architecture with facade pattern.
- Data serialization and validation.
- Unittests for facade and endpoints.

### 🛠 Technologies Used

| Layer        | Tools & Languages             |
|--------------|-------------------------------|
| Backend      | Python, Flask                 |
| Testing      | unittest, postman             |

### 📁 Project Structure

    v1/
    ├── app/
    │   ├── __init__.py
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── v1/
    │   │       ├── __init__.py
    │   │       ├── users.py
    │   │       ├── places.py
    │   │       ├── reviews.py
    │   │       ├── amenities.py
    │   ├── models/
    │   │   ├── __init__.py
    │   │   ├── user.py
    │   │   ├── place.py
    │   │   ├── review.py
    │   │   ├── amenity.py
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── facade.py
    │   ├── persistence/
    │   │   ├── __init__.py
    │   │   ├── repository.py
    │   ├── tests/
    │   │   ├──api_unittest_amenity.py
    │   │   ├──api_unittest_places.py
    │       ├──api_unittest_review.py
    │       ├──api_unittest_users.py
    │       ├──class_model_amenity_test.py
    │       ├──class_model_review_test.py
    │       ├──class_models_test.py
    │       ├──facade_unittest_amenity.py
    │       ├──facade_unittest_places.py
    │       ├──facade_unittest_review.py
    │       ├──facade_unittest_user.py
    ├── run.py
    ├── config.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md

### 🛠 Installation and running

#### Clone the repository
```bash
git clone https://github.com/andreamgrs/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```
#### Create a virtual environment 
```bash
cd v1/
python3 -m venv venv
source venv/bin/activate
```
#### Install requirements
```bash
pip install -r requirements.txt
```
#### Run the application and the API will start.
```bash
python3 run.py
# Visit: http://localhost:5000/api/v1/
```

### 🧪 Testing

This project uses Python’s built-in `unittest` framework to validate class models, API endpoints, and facade logic. Each test ensures that components behave correctly and integrate smoothly.

#### 🔹 Class Model Tests

Each model has its own test file named using the format: class_model_"name-of-model"_test.py
```bash
# Example with review test:
cd v1/
python3 -m app.tests.class_model_review_test
```

#### 🔹 API Endpoint Tests

Each model has its own test file named using the format: app/tests/api_unittest_"name-of-model".py
```bash
# Example with review test:
cd v1/
python3 -m unittest app/tests/api_unittest_review.py
```

#### 🔹 Facade Logic Tests

Each model has its own test file named using the format: app/tests/facade_unittest_"name-of-model".py
```bash
# Example with review test:
cd v1/
python3 -m unittest app/tests/facade_unittest_review.py
```

## 👥 Contributors
- Thannie Phan
- Sheeny Soulsby
- Andrea Munoz
