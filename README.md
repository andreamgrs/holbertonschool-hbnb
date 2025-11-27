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


### 🚧 V3 – Enhanced Backend with Authentication and Database Integration

In this phase we extend the backend of the application by introducing user authentication, authorization, and database integration using SQLAlchemy and SQLite for development.

- Authentication and Authorization using Flask-JWT-Extended and role-based access control with the is_admin attribute for specific endpoints.
- Database Integration
- Refactor all CRUD operations to interact with a persistent database.
- Database Design and Visualization using mermeid.js

### 🚀 V4 - Simple Web Client
In this phase, we build the front-end of your application using HTML5, CSS3, and JavaScript ES6, creating an interactive interface that connects with the back-end services developed earlier.

- Design user-friendly pages (Login, List of Places, Place Details, and Add Review).
- Implement secure client-side functionality with JWT-based authentication.
- Fetch API/AJAX to retrieve and display data, apply filtering on the list of places, restrict access to leave a review for authenticated users only, and ensure reviews cannot be submitted for owners of places while practicing modern web development techniques and session management.

## 🛠 Technologies Used

| Layer        | Tools & Languages                                                  |
|--------------|--------------------------------------------------------------------|
| Backend      | Python3, Flask, SQLAlchemy, SQLite, MySQL, JWT Authentication      |
| Testing      | unittest, postman                                                  |
| Frontend     | HTML5, CSS3, JavaScript ES6, Fetch API, Cookies for JWT storage    |


## 👥 Contributors
- Thannie Phan
- Sheeny Soulsby
- Andrea Munoz