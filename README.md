# 🏠 HBnB Project

Welcome to the HBnB project! A full-stack clone of the AirBnB web application, built to demonstrate learned capabilities of backend and frontend development, object-oriented programming, and deployment.

## 📌 Table of Contents

- [Description](#description)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributors](#contributors)

## 📖 Description

HBnB is a web-based application that allows users to create, update, and manage listings of places to stay. It mimics the core functionality of AirBnB, including user authentication, listing creation, and changes based on user interaction or data

This project is part of the Holberton School curriculum and is built in stages:
- V1
In this first part we focus on creating comprehensive technical documentation that will serve as the foundation for the development of the HBnB Evolution application.
- V2
In the second part we implement the core functionality of the application using Python and Flask. This will involve building the Presentation and Business logic layers, and defining essential classes, methods and API endpoints, based on the design developed in the previous part. 
- V3
- V4


## 🛠 Technologies Used

| Layer        | Tools & Languages             |
|--------------|-------------------------------|
| Backend      | Python, Flask                 |
| Testing      | unittest, postman             |

## Project Structure

 ```Hbnb
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
    │   │   ├──api_unittest_places.py
    │       ├──api_unittest_review.py
    │       ├──api_unittest_users.py
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
    ```