# 🏠 HBnB Project 

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
## Part 3 Enhanced Backend with Authentication and Database Integration

In this Part 3 of the HBnB Project! We focus on transforming the backend into a secure, persistent, and production-ready system. Where we implement user authentication, enforce access control, and migrate from in-memory storage to a robust database architecture using SQLAlchemy and SQLite with MySQL prepared for deployment.

### 🧱 Project Structure Summary
- Add password hashing to User model with bcrypt2
- Secure API with JWT authentication (Flask-JWT-Extended)
- Implement role-based access control (is_admin)
- Replace in-memory storage with SQLite using SQLAlchemy
- Map models (User, Place, Review, Amenity) to database tables
- Configure MySQL for production use
- Visualize schema with mermaid.js diagrams




## 👥 Contributors
- Thannie Phan
- Sheeny Soulsby
- Andrea Munoz