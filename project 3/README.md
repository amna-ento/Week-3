# Secure Customer Churn Prediction API

## Overview

This project combines **User Authentication** and **Machine Learning Model Deployment** into one secure API.

Users must first create an account and log in. After successful authentication, the API issues a JSON Web Token (JWT). This token is then used to access the machine learning prediction endpoints.

The machine learning model predicts whether a customer is likely to churn based on customer information.

---

## Features

- User Registration
- User Login
- JWT Authentication
- Protected API Endpoints
- Single Customer Prediction
- Batch Prediction
- Health Check Endpoint
- Pydantic Data Validation
- SQLAlchemy Database Integration

---

## Project Structure

```
project_3/
│
├── app/
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── dependencies.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── predictor.py
│   ├── schemas.py
│   └── security.py
│
├── churn_pipeline.pkl
├── users.db
├── .env
└── requirements.txt
```

---

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- python-jose
- Passlib (bcrypt)
- Pandas
- Scikit-learn
- Joblib
- Uvicorn

---

## Installation


### 1. Create a Virtual Environment

```bash
python3 -m venv .venv
```

---

### 2. Activate the Virtual Environment

macOS/Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable, install manually:

```bash
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install pandas
pip install scikit-learn
pip install joblib
pip install python-multipart
pip install email-validator
pip install "passlib[bcrypt]"
pip install "python-jose[cryptography]"
```

---

### 4. Environment Variables

Create a file named

```
.env
```

Add the following variables:

```bash
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Machine Learning Model

Place the trained model

```
churn_pipeline.pkl
```

inside the project root directory.

---

### 6. User Database

Ensure

```
users.db
```

exists in the project root.

If it does not exist, FastAPI will create it automatically when the application starts.

---

### 7. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will start on

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

---

## API Workflow

The API should be used in the following order:

1. Register a new user
2. Login
3. Receive JWT Token
4. Authorize using the token
5. Access protected prediction endpoints

Flow:

```
Register
      │
      ▼
Login
      │
      ▼
Receive JWT Token
      │
      ▼
Authorize
      │
      ▼
Predict Customer Churn
```

---

## API Endpoints

### Home

**GET /**

**Purpose**

Returns a welcome message indicating the API is running.

**Example curl**

```bash
curl http://127.0.0.1:8000/
```

**Expected Response**

```json
{
    "message": "Secure Customer Churn Prediction API is running!"
}
```

---

### Health Check

**GET /health**

**Purpose**

Checks whether the machine learning model has loaded successfully.

**Example curl**

```bash
curl http://127.0.0.1:8000/health
```

**Expected Response**

```json
{
    "status": "healthy",
    "model_loaded": true,
    "model_version": "1.0.0"
}
```

---

### Register User

**POST /register**

**Purpose**

Creates a new user account.

**Example curl**

```bash
curl -X POST http://127.0.0.1:8000/register \
-H "Content-Type: application/json" \
-d '{
    "username":"amna",
    "email":"amna@example.com",
    "password":"12345678"
}'
```

**Expected Response**

```json
{
    "id": 1,
    "username": "amna",
    "email": "amna@example.com"
}
```

---

### Login

**POST /login**

**Purpose**

Authenticates the user and returns a JWT access token.

**Example curl**

```bash
curl -X POST http://127.0.0.1:8000/login \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=amna&password=12345678"
```

**Expected Response**

```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

---

### Get User Profile

**GET /profile**

**Purpose**

Returns the information of the currently logged-in user.

This endpoint is protected and requires a valid JWT access token.

**Example curl**

```bash
curl -X GET http://127.0.0.1:8000/profile \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response**

```json
{
    "id": 1,
    "username": "amna",
    "email": "amna@example.com"
}
```

---

## Authorization

The prediction endpoints are protected.

Before calling them, include the JWT token in the request header.

**Header format**

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Without this header, the API returns

```json
{
    "detail": "Not authenticated"
}
```

---

## Predict Customer Churn

**POST /predict**

**Purpose**

Predicts whether a single customer is likely to churn.

This endpoint requires authentication.

**Example curl**

```bash
curl -X POST http://127.0.0.1:8000/predict \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "gender":"Female",
  "SeniorCitizen":0,
  "Partner":"Yes",
  "Dependents":"No",
  "tenure":12,
  "PhoneService":"Yes",
  "MultipleLines":"No",
  "InternetService":"Fiber optic",
  "OnlineSecurity":"No",
  "OnlineBackup":"Yes",
  "DeviceProtection":"No",
  "TechSupport":"No",
  "StreamingTV":"Yes",
  "StreamingMovies":"Yes",
  "Contract":"Month-to-month",
  "PaperlessBilling":"Yes",
  "PaymentMethod":"Electronic check",
  "MonthlyCharges":70.35,
  "TotalCharges":850.50
}'
```

**Expected Response**

```json
{
    "prediction": 1,
    "probability": 0.91
}
```

Where

- `prediction = 1` → Customer is likely to churn.
- `prediction = 0` → Customer is unlikely to churn.
- `probability` → Model confidence for the prediction.

---

## Batch Prediction

**POST /predict/batch**

**Purpose**

Predicts churn for multiple customers in a single request.

**Example curl**

```bash
curl -X POST http://127.0.0.1:8000/predict/batch \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "customers":[
    {
      "gender":"Female",
      "SeniorCitizen":0,
      "Partner":"Yes",
      "Dependents":"No",
      "tenure":12,
      "PhoneService":"Yes",
      "MultipleLines":"No",
      "InternetService":"Fiber optic",
      "OnlineSecurity":"No",
      "OnlineBackup":"Yes",
      "DeviceProtection":"No",
      "TechSupport":"No",
      "StreamingTV":"Yes",
      "StreamingMovies":"Yes",
      "Contract":"Month-to-month",
      "PaperlessBilling":"Yes",
      "PaymentMethod":"Electronic check",
      "MonthlyCharges":70.35,
      "TotalCharges":850.50
    }
  ]
}'
```

**Expected Response**

```json
[
    {
        "prediction": 1,
        "probability": 0.91
    }
]
```

---

## Logging

Every prediction request is logged.

Each log entry contains

- Timestamp
- SHA-256 hash of the input data
- Prediction result
- Prediction latency (milliseconds)

Logging helps in

- Monitoring requests
- Auditing predictions
- Measuring API performance
- Debugging issues

---

## Authentication Flow

```
Client
   │
   ▼
POST /register
   │
   ▼
POST /login
   │
   ▼
Receive JWT Token
   │
   ▼
Authorization Header
   │
   ▼
JWT Validation
   │
   ▼
Access Protected Endpoints
```

---

## Common HTTP Status Codes

| Status Code | Meaning                                         |
| ------------ | ------------------------------------------------ |
| 200          | Request completed successfully                   |
| 201          | Resource created successfully (if applicable)     |
| 400          | Invalid request or duplicate user                 |
| 401          | Unauthorized or invalid JWT token                  |
| 404          | Endpoint not found                                 |
| 422          | Request validation failed due to invalid input     |
| 500          | Internal server error                              |

---

## Example Error Responses

### User already exists

```json
{
    "detail": "Username already exists"
}
```

---

### Invalid login credentials

```json
{
    "detail": "Invalid username or password"
}
```

---

### Missing JWT Token

```json
{
    "detail": "Not authenticated"
}
```

---

### Invalid JWT Token

```json
{
    "detail": "Could not validate credentials"
}
```

---

### Validation Error

```json
{
    "detail": [
        {
            "loc": ["body", "MonthlyCharges"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

---

## Security Features

- Passwords are securely hashed using **bcrypt** before being stored.
- Plain-text passwords are never saved in the database.
- JWT tokens are used for user authentication.
- Protected endpoints require a valid access token.
- Sensitive configuration values (such as `SECRET_KEY`) are stored in a `.env` file.
- Password verification is performed using secure hash comparison.
- User authentication is handled through FastAPI dependency injection.

---


## Conclusion

This project demonstrates how to securely deploy a machine learning model as a production-ready web service. It integrates user authentication with JWT, protects prediction endpoints, validates incoming data using Pydantic, logs prediction requests, and serves a trained churn prediction model through FastAPI. The combination of authentication and model serving reflects a common real-world deployment pattern, where only authorized users can access machine learning services securely and efficiently.
