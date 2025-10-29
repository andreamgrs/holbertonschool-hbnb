# 🏠 HBnB Project

Welcome to the HBnB project! A full-stack clone of the AirBnB web application, built to demonstrate learned capabilities of backend and frontend development, object-oriented programming, and deployment.

## 📖 Description

HBnB is a web-based application that allows users to create, update, and manage listings of places to stay. It mimics the core functionality of AirBnB, including user authentication, listing creation, and changes based on user interaction or data.

## 🏗️ Project Overview

### 📚 V1 – Documentation Foundation

This phase defines the architecture and business logic for HBnB Evolution.

- Core entities: User, Place, Review, Amenity
- Business rules and relationships
- Layered architecture: Presentation, Business Logic, Persistence
- UML diagrams: package, class, and API sequences

The goal is to produce clear, implementation-ready documentation that guides development in later stages.


### 🧩 V2 – Core Application Logic

Implements HBnB Evolution’s backend using Python and Flask.

- Core models (User, Place, Review, Amenity)
- RESTful API endpoints with flask-restx.
- Layered architecture with facade pattern.
- Data serialization and validation.
- Unittests for facade and endpoints.


### 🚧 V3 – [Coming Soon]

### 🚀 V4 – [Coming Soon]

## 🛠 Technologies Used

| Layer        | Tools & Languages             |
|--------------|-------------------------------|
| Backend      | Python, Flask                 |
| Testing      | unittest, postman             |

## 📁 Project Structure

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

## 🛠 Installation and running 
```bash
cd v1/
pip install -r requirements.txt
python3 run.py
# Visit: http://localhost:5000/api/v1/
```
## 🧪 Testing

This project uses Python’s built-in `unittest` framework to validate class models, API endpoints, and facade logic. Each test ensures that components behave correctly and integrate smoothly.

### 🔹 Class Model Tests

Each model has its own test file named using the format: class_model_<name-of-model>_test.py
```bash
# Example with review test:
cd v1/
python3 -m app.tests.class_model_review_test
```

### 🔹 API Endpoint Tests

Each model has its own test file named using the format: app/tests/api_unittest_<name-of-model>.py
```bash
# Example with review test:
cd v1/
python3 -m unittest app/tests/api_unittest_review.py
```

### 🔹 Facade LOgic Tests

Each model has its own test file named using the format: app/tests/facade_unittest_<name-of-model>.py
```bash
# Example with review test:
cd v1/
python3 -m unittest app/tests/facade_unittest_review.py
```


## 👥 Contributors
- Thannie Phan
- Sheeny Soulsby
- Andrea Munoz