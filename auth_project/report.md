# Authentication Service Project Report

## Overview

This project is an authentication service that allows users to:

- Register an account
- Log in securely
- View their profile information

The system is designed to safely store user accounts, securely verify passwords, and issue temporary access tokens for protected operations.

---

# Modules and Their Responsibilities

## 1. Application Setup

### Responsibility:
Starts the application and makes it available to receive requests.

### Features:
- Initializes the service
- Creates the user database structure before handling requests
- Provides a simple welcome endpoint to confirm that the service is running

---

## 2. Authentication Routes

### Responsibility:
Provides user-facing authentication actions.

### Available Operations:
- Register a new account
- Log in with existing credentials
- Retrieve the currently logged-in user's profile

### Handles:
- Incoming request validation
- Successful responses
- Authentication errors

---

## 3. User Data Model

### Responsibility:
Defines the internal structure of a user account.

### User Contains:

- Unique user ID
- Username
- Email address
- Password 

This model is used whenever the system reads or writes user information from the database.

---

## 4. Request and Response Validation

### Responsibility:
Defines the structure of incoming and outgoing data.

### Validation Rules:

- Username length requirements
- Valid email format
- Minimum password length

### Also Defines:

- User response format
- Access token response format

This ensures that only valid data enters and leaves the system.

---

## 5. Database Operations

### Responsibility:
Handles direct communication with the database.

### Functions Include:

- Find user by username
- Find user by email
- Create a new user
- Verify user login credentials

This keeps database logic separate from the main application logic.

---

## 6. Database Connection

### Responsibility:
Configures the database engine and manages database sessions.

### Features:

- Creates a local database file
- Provides database connections to application components
- Ensures sessions are closed properly after use

---

## 7. Authentication Dependency

### Responsibility:
Identifies the current user making a request.

### Process:

1. Reads the access token from the request
2. Validates the token
3. Finds the matching user account

If:
- The token is invalid
- The user does not exist

Then access is denied.

---

## 8. Security

### Responsibility:
Handles all security-related operations.

### Includes:

- Hashing plain text passwords
- Comparing entered passwords with stored hashes
- Creating signed access tokens
- Validating tokens during future requests

The system never stores raw passwords.

---

# What Was Implemented

The authentication service includes:

- User registration with duplicate username/email prevention
- Secure password hashing
- Login functionality with temporary access tokens
- Protected profile endpoint requiring valid authentication
- Clean project structure separating:

  - Application startup
  - Authentication routes
  - User models
  - Data validation
  - Database operations
  - Database connection
  - Authentication logic
  - Security handling

---

# How the Flow Works

## User Registration Flow

1. User sends registration information

2. System validates the input data

3. System checks for duplicate usernames or emails

4. Password is converted into a secure hash

5. User account is stored in the database


---

## User Login Flow

1. User provides username and password

2. System verifies the password

3. A secure access token is generated

4. Token is returned to the user

5. The token is used for future protected requests


---

## Profile Access Flow

1. User sends a request with the access token

2. System validates the token

3. System identifies the user

4. User profile information is returned

---

# Summary

This project is a simple but complete authentication backend.

It separates responsibilities into clear modules, uses validation to maintain correct data, and applies industry-standard security practices for password storage and token-based authentication.

The final system can:

- Register users
- Authenticate users securely
- Generate access tokens
- Protect user-specific operations
- Manage user data through a structured backend architecture